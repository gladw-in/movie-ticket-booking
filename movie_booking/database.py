"""Connects to MySQL, creates the tables and stores customer accounts."""

import re
from contextlib import contextmanager

import mysql.connector

from .accounts import Account, AccountExists
from .paths import SCHEMA_SQL

_IDENTIFIER = re.compile(r"^[A-Za-z0-9_$]+$")


class DatabaseError(Exception):
    pass


def _quote_identifier(name):
    if not _IDENTIFIER.match(name):
        raise DatabaseError(f"Invalid database name: {name!r}")
    return f"`{name}`"


@contextmanager
def connect(settings, *, use_database=True):
    options = dict(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password or "",
    )
    if use_database:
        options["database"] = settings.database
    try:
        connection = mysql.connector.connect(**options)
    except mysql.connector.Error as exc:
        raise DatabaseError(f"Could not connect to MySQL: {exc}") from exc
    try:
        yield connection
        connection.commit()
    except mysql.connector.Error as exc:
        connection.rollback()
        raise DatabaseError(f"Database error: {exc}") from exc
    finally:
        connection.close()


def schema_statements(sql=None):
    sql = SCHEMA_SQL.read_text(encoding="utf-8") if sql is None else sql
    lines = [line for line in sql.splitlines() if not line.strip().startswith("--")]
    return [stmt.strip() for stmt in "\n".join(lines).split(";") if stmt.strip()]


def create_database(settings):
    with connect(settings, use_database=False) as conn:
        conn.cursor().execute(
            f"CREATE DATABASE IF NOT EXISTS {_quote_identifier(settings.database)}"
        )


def create_tables(settings):
    with connect(settings) as conn:
        cursor = conn.cursor()
        for statement in schema_statements():
            cursor.execute(statement)


def ensure_schema(settings):
    create_database(settings)
    create_tables(settings)


class MySQLAccountRepository:
    def __init__(self, settings):
        self._settings = settings

    def get(self, username):
        with connect(self._settings) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, phno, `pass` FROM acc WHERE username = %s",
                (username,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return Account(username=row[0], phone=row[1] or "", password_hash=row[2] or "")

    def add(self, account):
        try:
            with connect(self._settings) as conn:
                conn.cursor().execute(
                    "INSERT INTO acc (username, phno, `pass`) VALUES (%s, %s, %s)",
                    (account.username, account.phone, account.password_hash),
                )
        except DatabaseError as exc:
            if isinstance(exc.__cause__, mysql.connector.IntegrityError):
                raise AccountExists("That username is already taken.") from exc
            raise

    def set_password_hash(self, username, password_hash):
        with connect(self._settings) as conn:
            conn.cursor().execute(
                "UPDATE acc SET `pass` = %s WHERE username = %s",
                (password_hash, username),
            )

    def delete(self, username):
        with connect(self._settings) as conn:
            conn.cursor().execute("DELETE FROM acc WHERE username = %s", (username,))
