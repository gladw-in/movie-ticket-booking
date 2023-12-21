"""Tests for sign-up, log-in and password reset."""

import pytest

from movie_booking import security
from movie_booking.accounts import (
    Account,
    AccountExists,
    AccountService,
    IdentityMismatch,
    InvalidCredentials,
)
from movie_booking.validation import ValidationError

from .fakes import FakeRepo


@pytest.fixture
def repo():
    return FakeRepo()


@pytest.fixture
def service(repo):
    return AccountService(repo)


def sign_up(service, name="tanishk", phone="9820229482", pw="pass1234"):
    return service.sign_up(name, phone, pw, pw)


def test_sign_up_stores_a_hash_not_the_password(service, repo):
    sign_up(service)
    stored = repo.rows["tanishk"].password_hash
    assert stored != "pass1234" and security.is_hashed(stored)


def test_sign_up_rejects_bad_input_without_touching_the_repo(service, repo):
    with pytest.raises(ValidationError):
        service.sign_up("ab", "9820229482", "pass1234", "pass1234")
    with pytest.raises(ValidationError):
        service.sign_up("tanishk", "123", "pass1234", "pass1234")
    with pytest.raises(ValidationError):
        service.sign_up("tanishk", "9820229482", "pass1234", "different")
    assert repo.rows == {}


def test_duplicate_username_is_rejected(service):
    sign_up(service)
    with pytest.raises(AccountExists):
        sign_up(service)


def test_log_in(service):
    sign_up(service)
    assert service.log_in("tanishk", "pass1234").username == "tanishk"
    assert service.log_in("  tanishk ", "pass1234").username == "tanishk"


def test_log_in_failures_do_not_reveal_which_part_was_wrong(service):
    sign_up(service)
    with pytest.raises(InvalidCredentials) as wrong_pw:
        service.log_in("tanishk", "nope")
    with pytest.raises(InvalidCredentials) as no_user:
        service.log_in("ghost", "pass1234")
    assert str(wrong_pw.value) == str(no_user.value)


def test_log_in_requires_both_fields(service):
    for user, pw in [("", "x"), ("tanishk", "")]:
        with pytest.raises(InvalidCredentials):
            service.log_in(user, pw)


def test_legacy_plaintext_account_is_upgraded_on_login(service, repo):
    repo.rows["Admin"] = Account("Admin", "9821024582", "123456")
    service.log_in("Admin", "123456")
    assert security.is_hashed(repo.rows["Admin"].password_hash)
    assert service.log_in("Admin", "123456")


def test_reset_password_needs_matching_phone(service):
    sign_up(service)
    with pytest.raises(IdentityMismatch):
        service.reset_password("tanishk", "0000000000", "newpass1", "newpass1")
    with pytest.raises(IdentityMismatch):
        service.reset_password("ghost", "9820229482", "newpass1", "newpass1")


def test_reset_password(service):
    sign_up(service)
    service.reset_password("tanishk", "9820229482", "newpass1", "newpass1")
    assert service.log_in("tanishk", "newpass1")
    with pytest.raises(InvalidCredentials):
        service.log_in("tanishk", "pass1234")


def test_reset_validates_the_new_password(service):
    sign_up(service)
    with pytest.raises(ValidationError):
        service.reset_password("tanishk", "9820229482", "ab", "ab")


def test_legacy_phone_with_trailing_space_still_matches(service, repo):
    repo.rows["Dhruv"] = Account("Dhruv", "9822724582 ", "123456")
    assert service.verify_identity("Dhruv", "9822724582")


def test_delete(service, repo):
    sign_up(service)
    service.delete_account("tanishk")
    assert repo.rows == {}


def test_username_suggestions_are_distinct_and_contain_the_name(service):
    suggestions = service.suggest_usernames("tanishk")
    assert len(set(suggestions)) == 2 and all("tanishk" in s for s in suggestions)


def test_username_suggestions_are_always_valid_usernames(service):
    from movie_booking.validation import validate_username

    for name in ("x" * 20, "x" * 18, "abcd", "Glad432"):
        for _ in range(25):
            for suggestion in service.suggest_usernames(name):
                validate_username(suggestion)
