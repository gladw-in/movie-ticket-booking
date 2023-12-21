"""Tests for the sign-up and password reset input checks."""

import pytest

from movie_booking import validation as v


@pytest.mark.parametrize("name", ["abcd", "Glad432", "a_b.c", "x" * 20])
def test_valid_usernames(name):
    assert v.validate_username(name) == name


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
        "abc",
        "x" * 21,
        "has space",
        "bad@name",
        "semi;colon",
        'quo"te',
        "back\\slash",
    ],
)
def test_invalid_usernames(name):
    with pytest.raises(v.ValidationError):
        v.validate_username(name)


@pytest.mark.parametrize(
    "phone", ["", "12345", "12345678901", "98229a4582", "+919822924", "\u0661" * 10]
)
def test_invalid_phones(phone):
    with pytest.raises(v.ValidationError):
        v.validate_phone(phone)


def test_valid_phone():
    assert v.validate_phone("9822924582") == "9822924582"


def test_password_rules():
    assert v.validate_new_password("abcd", "someone")
    for bad in ["", "abc", "x" * 21, "has space"]:
        with pytest.raises(v.ValidationError):
            v.validate_new_password(bad)
    with pytest.raises(v.ValidationError):
        v.validate_new_password("sameas", "sameas")


def test_confirmation():
    v.validate_confirmation("abcd", "abcd")
    for bad in ["", "abce"]:
        with pytest.raises(v.ValidationError):
            v.validate_confirmation("abcd", bad)
