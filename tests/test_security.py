"""Tests for password hashing and checking."""

from movie_booking import security


def test_hash_verifies_and_is_salted():
    first, second = security.hash_password("secret1"), security.hash_password("secret1")
    assert first != second
    assert security.verify_password("secret1", first)
    assert not security.verify_password("secret2", first)


def test_legacy_plaintext_is_accepted_and_flagged_for_rehash():
    assert security.verify_password("123456", "123456")
    assert not security.verify_password("654321", "123456")
    assert security.needs_rehash("123456")


def test_current_hash_does_not_need_rehash(monkeypatch):
    stored = security.hash_password("abcd")
    assert not security.needs_rehash(stored)
    monkeypatch.setattr(security, "ITERATIONS", 5_000)
    assert security.needs_rehash(stored)


def test_empty_or_malformed_values_never_verify():
    assert not security.verify_password("x", None)
    assert not security.verify_password("", "")
    assert not security.verify_password("x", "pbkdf2_sha256$10$zz$zz")
