"""Tests for the bank simulator storage and rules."""

import pytest

from movie_booking.bank import (
    AuthenticationFailed,
    BankError,
    BankStore,
    InsufficientFunds,
    format_money,
    parse_amount,
)
from movie_booking.bank.rules import (
    validate_bank_password,
    validate_bank_username,
    validate_profile,
)
from movie_booking.bank.store import import_legacy_files
from movie_booking.validation import ValidationError

PW = "Passw0rd_"
PROFILE = dict(
    phone="9822924582",
    country="India",
    state="Goa",
    pincode="403001",
    age="21",
    gender="Male",
    account_type="Savings Account",
)


@pytest.fixture
def bank(tmp_path):
    store = BankStore(tmp_path / "bank.sqlite3")
    yield store
    store.close()


@pytest.fixture
def bob(bank):
    bank.register("bob", PW, PW)
    return bank


@pytest.mark.parametrize(
    "text,cents",
    [("100", 10000), ("99.5", 9950), (" 0.01 ", 1), ("1,5".replace(",", "."), 150)],
)
def test_parse_amount(text, cents):
    assert parse_amount(text) == cents


@pytest.mark.parametrize(
    "text", ["", "abc", "0", "-5", "1.005", "NaN", "inf", "1e30", "5 0"]
)
def test_parse_amount_rejects(text):
    with pytest.raises(ValidationError):
        parse_amount(text)


def test_format_money():
    assert format_money(123456) == "\u20b91,234.56" and format_money(0) == "\u20b90.00"


def test_register_and_authenticate(bob):
    assert bob.authenticate("bob", PW) == "bob"
    assert bob.authenticate("BOB", PW) == "bob"
    with pytest.raises(AuthenticationFailed):
        bob.authenticate("bob", "wrong")
    with pytest.raises(AuthenticationFailed):
        bob.authenticate("nobody", PW)


def test_duplicate_names_are_rejected_case_insensitively(bob):
    with pytest.raises(BankError):
        bob.register("BOB", PW, PW)


@pytest.mark.parametrize("name", ["", "has space", "a_b", "a@b", "a$b", "x" * 31])
def test_bad_usernames(name):
    with pytest.raises(ValidationError):
        validate_bank_username(name)


@pytest.mark.parametrize(
    "pw",
    ["", "Ab1_", "alllower1_", "ALLUPPER1_", "NoDigits_", "NoSpecial1a", "Has 1_Space"],
)
def test_bad_passwords(pw):
    with pytest.raises(ValidationError):
        validate_bank_password(pw)


def test_passwords_must_match(bank):
    with pytest.raises(ValidationError):
        bank.register("bob", PW, PW + "x")


def test_passwords_are_not_stored_in_plaintext(bob):
    stored = bob._conn.execute("SELECT password_hash FROM accounts").fetchone()[0]
    assert PW not in stored and stored.startswith("pbkdf2_sha256$")


def test_path_like_names_cannot_escape_anything(bank):
    bank.register("../../etc", PW, PW)
    assert bank.exists("../../etc")


def test_deposit_withdraw_and_history(bob):
    assert bob.deposit("bob", 10000) == 10000
    assert bob.withdraw("bob", 2550) == 7450
    kinds = [t.kind for t in bob.history("bob")]
    assert kinds == ["Account created", "Deposit", "Withdraw"]
    assert bob.history("bob")[-1].balance_after_cents == 7450


def test_cannot_overdraw_and_failure_changes_nothing(bob):
    bob.deposit("bob", 1000)
    with pytest.raises(InsufficientFunds):
        bob.withdraw("bob", 1001)
    assert bob.balance("bob") == 1000 and len(bob.history("bob")) == 2


def test_exact_balance_can_be_spent(bob):
    bob.deposit("bob", 70000)
    assert bob.charge("bob", PW, 70000, "bookmyshow.com") == 0


def test_charge_checks_credentials_and_funds(bob):
    bob.deposit("bob", 50000)
    with pytest.raises(AuthenticationFailed):
        bob.charge("bob", "wrong", 100, "x")
    with pytest.raises(InsufficientFunds):
        bob.charge("bob", PW, 50001, "x")
    assert bob.balance("bob") == 50000
    assert bob.charge("bob", PW, 45000, "bookmyshow.com") == 5000
    last = bob.history("bob")[-1]
    assert (last.kind, last.amount_cents, last.note) == (
        "Payment",
        45000,
        "bookmyshow.com",
    )


def test_non_positive_amounts_are_rejected(bob):
    for call in (bob.deposit, bob.withdraw):
        with pytest.raises(ValidationError):
            call("bob", 0)
        with pytest.raises(ValidationError):
            call("bob", -5)


def test_no_float_drift(bob):
    for _ in range(10):
        bob.deposit("bob", parse_amount("0.10"))
    assert bob.balance("bob") == 100


def test_profile_round_trip_and_update(bob):
    assert bob.get_profile("bob") is None
    bob.save_profile("bob", PROFILE)
    assert bob.get_profile("bob") == PROFILE
    bob.save_profile("bob", {**PROFILE, "state": "Kerala"})
    assert bob.get_profile("bob")["state"] == "Kerala"


@pytest.mark.parametrize(
    "change",
    [
        {"phone": "123"},
        {"pincode": "abc"},
        {"age": "0"},
        {"gender": "Select"},
        {"account_type": "Select"},
        {"country": ""},
    ],
)
def test_invalid_profiles(change):
    with pytest.raises(ValidationError):
        validate_profile({**PROFILE, **change})


def test_reset_password_requires_the_phone_on_file(bob):
    with pytest.raises(BankError):
        bob.reset_password("bob", "9822924582", "Newpass1_", "Newpass1_")
    bob.save_profile("bob", PROFILE)
    with pytest.raises(BankError):
        bob.reset_password("bob", "0000000000", "Newpass1_", "Newpass1_")
    bob.reset_password("bob", "9822924582", "Newpass1_", "Newpass1_")
    assert bob.authenticate("bob", "Newpass1_")
    with pytest.raises(AuthenticationFailed):
        bob.authenticate("bob", PW)


def test_admin_password_is_set_once_and_verified(bank):
    assert not bank.has_admin() and not bank.verify_admin("anything")
    with pytest.raises(ValidationError):
        bank.set_admin_password("short", "short")
    bank.set_admin_password("longenough", "longenough")
    assert (
        bank.has_admin()
        and bank.verify_admin("longenough")
        and not bank.verify_admin("nope")
    )
    with pytest.raises(BankError):
        bank.set_admin_password("another-one", "another-one")


def test_account_listing_never_exposes_passwords(bob):
    bob.deposit("bob", 500)
    [summary] = bob.list_accounts()
    assert (summary.name, summary.balance_cents) == ("bob", 500)
    assert not hasattr(summary, "password_hash")


def test_import_legacy_files(bank, tmp_path):
    legacy = tmp_path / "old"
    legacy.mkdir()
    (legacy / "alice").write_text("alice\nOldPass1_\n1500.5")
    (legacy / "alice's transaction history").write_text("created")
    (legacy / "alice's personal info").write_text("\n".join(PROFILE.values()) + "\n")
    (legacy / "README.txt").write_text("not an account")
    (legacy / "broken").write_text("broken\npw")
    (legacy / "broken's transaction history").write_text("")

    assert import_legacy_files(bank, legacy) == ["alice"]
    assert bank.balance("alice") == 150050
    assert bank.authenticate("alice", "OldPass1_")
    assert bank.get_profile("alice")["state"] == "Goa"
    assert import_legacy_files(bank, legacy) == []


def test_a_locked_database_is_reported_as_a_bank_error_and_recovers(tmp_path):
    first = BankStore(tmp_path / "shared.db")
    first.register("bob", PW, PW)
    second = BankStore(tmp_path / "shared.db", timeout=0.1)
    first._conn.execute("BEGIN IMMEDIATE")
    with pytest.raises(BankError, match="busy"):
        second.deposit("bob", 100)
    with pytest.raises(BankError, match="busy"):
        second.charge("bob", PW, 100, "x")
    first._conn.execute("ROLLBACK")
    assert second.deposit("bob", 100) == 100
    first.close()
    second.close()


def test_a_failed_operation_leaves_no_half_finished_transaction(bob):
    with pytest.raises(InsufficientFunds):
        bob.withdraw("bob", 1)
    assert not bob._conn.in_transaction
    assert bob.deposit("bob", 5) == 5
