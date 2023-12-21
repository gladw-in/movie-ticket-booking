"""Stores bank accounts, balances and transactions in an SQLite file."""

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .. import security
from ..validation import ValidationError
from . import rules


class BankError(Exception):
    pass


class AccountExists(BankError):
    pass


class AuthenticationFailed(BankError):
    pass


class InsufficientFunds(BankError):
    pass


_SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    name          TEXT PRIMARY KEY COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    balance_cents INTEGER NOT NULL DEFAULT 0 CHECK (balance_cents >= 0),
    created_at    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
    name         TEXT PRIMARY KEY COLLATE NOCASE REFERENCES accounts(name) ON DELETE CASCADE,
    phone TEXT, country TEXT, state TEXT, pincode TEXT, age TEXT, gender TEXT, account_type TEXT
);
CREATE TABLE IF NOT EXISTS transactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL COLLATE NOCASE REFERENCES accounts(name) ON DELETE CASCADE,
    kind                TEXT NOT NULL,
    amount_cents        INTEGER NOT NULL DEFAULT 0,
    balance_after_cents INTEGER NOT NULL,
    note                TEXT NOT NULL DEFAULT '',
    created_at          TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
"""

PROFILE_FIELDS = (
    "phone",
    "country",
    "state",
    "pincode",
    "age",
    "gender",
    "account_type",
)


@dataclass(frozen=True)
class AccountSummary:
    name: str
    balance_cents: int
    created_at: str


@dataclass(frozen=True)
class Transaction:
    created_at: str
    kind: str
    amount_cents: int
    balance_after_cents: int
    note: str

    def describe(self):
        amount = (
            f"  {rules.format_money(self.amount_cents)}" if self.amount_cents else ""
        )
        note = f"  {self.note}" if self.note else ""
        return (
            f"{self.created_at}  {self.kind}{amount}{note}  "
            f"(balance {rules.format_money(self.balance_after_cents)})"
        )


def _now():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class BankStore:
    def __init__(self, path, *, timeout=5.0):
        self._conn = sqlite3.connect(str(path), isolation_level=None, timeout=timeout)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(_SCHEMA)

    def close(self):
        self._conn.close()

    @contextmanager
    def _transaction(self):
        try:
            self._conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as exc:
            raise BankError(
                "The bank is busy right now. Please try again in a moment."
            ) from exc
        try:
            yield self._conn
            self._conn.execute("COMMIT")
        except BaseException as exc:
            if self._conn.in_transaction:
                self._conn.execute("ROLLBACK")
            if isinstance(exc, sqlite3.Error):
                raise BankError(
                    "The bank could not complete that request. Please try again."
                ) from exc
            raise

    def _row(self, name):
        return self._conn.execute(
            "SELECT * FROM accounts WHERE name = ?", (name,)
        ).fetchone()

    def exists(self, name):
        return self._row(name) is not None

    def register(self, name, password, confirmation):
        rules.validate_bank_username(name)
        rules.validate_bank_password(password, confirmation)
        with self._transaction() as conn:
            if conn.execute(
                "SELECT 1 FROM accounts WHERE name = ?", (name,)
            ).fetchone():
                raise AccountExists("An account with that name already exists.")
            conn.execute(
                "INSERT INTO accounts (name, password_hash, balance_cents, created_at) VALUES (?, ?, 0, ?)",
                (name, security.hash_password(password), _now()),
            )
            self._log(conn, name, "Account created", 0, 0)

    def add_imported_account(self, name, password, cents):
        cents = max(cents, 0)
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO accounts (name, password_hash, balance_cents, created_at) VALUES (?, ?, ?, ?)",
                (name, security.hash_password(password), cents, _now()),
            )
            self._log(conn, name, "Imported from legacy bank", 0, cents)

    def authenticate(self, name, password):
        row = self._row(name)
        if row is None or not security.verify_password(password, row["password_hash"]):
            raise AuthenticationFailed("Wrong account name or password.")
        return row["name"]

    def balance(self, name):
        row = self._row(name)
        if row is None:
            raise BankError("No such account.")
        return row["balance_cents"]

    def list_accounts(self):
        rows = self._conn.execute(
            "SELECT name, balance_cents, created_at FROM accounts ORDER BY name"
        ).fetchall()
        return [
            AccountSummary(r["name"], r["balance_cents"], r["created_at"]) for r in rows
        ]

    def log_event(self, name, note):
        with self._transaction() as conn:
            self._log(conn, name, note, 0, self._balance(conn, name))

    @staticmethod
    def _balance(conn, name):
        row = conn.execute(
            "SELECT balance_cents FROM accounts WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            raise BankError("No such account.")
        return row[0]

    @staticmethod
    def _log(
        conn,
        name,
        kind,
        amount,
        balance_after,
        note="",
    ):
        conn.execute(
            "INSERT INTO transactions (name, kind, amount_cents, balance_after_cents, note, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (name, kind, amount, balance_after, note, _now()),
        )

    def _apply(self, name, delta, kind, note=""):
        with self._transaction() as conn:
            current = self._balance(conn, name)
            updated = current + delta
            if updated < 0:
                raise InsufficientFunds("Insufficient funds.")
            conn.execute(
                "UPDATE accounts SET balance_cents = ? WHERE name = ?", (updated, name)
            )
            self._log(conn, name, kind, abs(delta), updated, note)
            return updated

    def deposit(self, name, cents):
        if cents <= 0:
            raise ValidationError("The amount must be greater than zero.")
        return self._apply(name, cents, "Deposit")

    def withdraw(self, name, cents):
        if cents <= 0:
            raise ValidationError("The amount must be greater than zero.")
        return self._apply(name, -cents, "Withdraw")

    def charge(self, name, password, cents, note):
        canonical = self.authenticate(name, password)
        if cents <= 0:
            raise ValidationError("The amount must be greater than zero.")
        return self._apply(canonical, -cents, "Payment", note)

    def history(self, name):
        rows = self._conn.execute(
            "SELECT created_at, kind, amount_cents, balance_after_cents, note"
            " FROM transactions WHERE name = ? ORDER BY id",
            (name,),
        ).fetchall()
        return [Transaction(*tuple(r)) for r in rows]

    def get_profile(self, name):
        row = self._conn.execute(
            "SELECT * FROM profiles WHERE name = ?", (name,)
        ).fetchone()
        return (
            None
            if row is None
            else {field: row[field] or "" for field in PROFILE_FIELDS}
        )

    def save_profile(self, name, values):
        clean = rules.validate_profile(values)
        columns = ", ".join(PROFILE_FIELDS)
        marks = ", ".join("?" for _ in PROFILE_FIELDS)
        updates = ", ".join(f"{f} = excluded.{f}" for f in PROFILE_FIELDS)
        with self._transaction() as conn:
            self._balance(conn, name)
            conn.execute(
                f"INSERT INTO profiles (name, {columns}) VALUES (?, {marks})"
                f" ON CONFLICT(name) DO UPDATE SET {updates}",
                (name, *(clean[f] for f in PROFILE_FIELDS)),
            )

    def reset_password(self, name, phone, new_password, confirmation):
        profile = self.get_profile(name)
        if not profile or not profile["phone"] or profile["phone"] != phone.strip():
            raise BankError(
                "The phone number does not match the one on file. "
                "(Add your personal info after logging in so you can reset later.)"
            )
        rules.validate_bank_password(new_password, confirmation)
        with self._transaction() as conn:
            conn.execute(
                "UPDATE accounts SET password_hash = ? WHERE name = ?",
                (security.hash_password(new_password), name),
            )
            self._log(conn, name, "Password reset", 0, self._balance(conn, name))

    def has_admin(self):
        return (
            self._conn.execute("SELECT 1 FROM meta WHERE key = 'admin_hash'").fetchone()
            is not None
        )

    def set_admin_password(self, password, confirmation):
        if self.has_admin():
            raise BankError("An admin password is already set.")
        if len(password) < 8:
            raise ValidationError("The admin password must be at least 8 characters.")
        if password != confirmation:
            raise ValidationError("The passwords do not match.")
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO meta (key, value) VALUES ('admin_hash', ?)",
                (security.hash_password(password),),
            )

    def verify_admin(self, password):
        row = self._conn.execute(
            "SELECT value FROM meta WHERE key = 'admin_hash'"
        ).fetchone()
        return row is not None and security.verify_password(password, row["value"])


def import_legacy_files(store, directory):
    directory = Path(directory)
    imported = []
    for history in sorted(directory.glob("*'s transaction history")):
        name = history.name[: -len("'s transaction history")]
        account_file = directory / name
        if not account_file.is_file() or store.exists(name):
            continue
        lines = account_file.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) < 3:
            continue
        try:
            cents = int((Decimal(lines[2].strip()) * 100).to_integral_value())
        except InvalidOperation:
            continue
        store.add_imported_account(name, lines[1], cents)
        info_file = directory / f"{name}'s personal info"
        if info_file.is_file():
            parts = info_file.read_text(encoding="utf-8", errors="replace").splitlines()
            if len(parts) >= 7:
                try:
                    store.save_profile(
                        name, dict(zip(PROFILE_FIELDS, parts[:7], strict=True))
                    )
                except ValidationError:
                    pass
        imported.append(name)
    return imported
