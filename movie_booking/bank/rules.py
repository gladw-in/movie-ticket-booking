"""Reads and shows money amounts and checks bank inputs."""

import re
from decimal import Decimal, InvalidOperation

from ..validation import ValidationError

MAX_AMOUNT_CENTS = 100_000_000 * 100
GENDERS = ("Male", "Female", "Other")
ACCOUNT_TYPES = (
    "Savings Account",
    "Recurring Deposit",
    "Current Account",
    "Fixed Deposit",
)


def parse_amount(text):
    text = (text or "").strip()
    if not text:
        raise ValidationError("Amount is required.")
    try:
        amount = Decimal(text)
    except InvalidOperation:
        raise ValidationError("Enter a valid amount.") from None
    if not amount.is_finite():
        raise ValidationError("Enter a valid amount.")
    if amount <= 0:
        raise ValidationError("The amount must be greater than zero.")
    cents = amount * 100
    if cents != cents.to_integral_value():
        raise ValidationError("Use at most two decimal places.")
    if cents > MAX_AMOUNT_CENTS:
        raise ValidationError("That amount is too large.")
    return int(cents)


def format_money(cents):
    return f"\u20b9{Decimal(cents) / 100:,.2f}"


def validate_bank_username(name):
    if not name:
        raise ValidationError("All fields are required.")
    if re.search(r"\s", name):
        raise ValidationError("Spaces are not allowed in the username.")
    if re.search(r"[_@$]", name):
        raise ValidationError("The username cannot contain _, @ or $.")
    if len(name) > 30:
        raise ValidationError("The username must be at most 30 characters.")
    return name


def validate_bank_password(password, confirmation=None):
    if not password:
        raise ValidationError("All fields are required.")
    if re.search(r"\s", password):
        raise ValidationError("Spaces are not allowed in the password.")
    if len(password) < 5:
        raise ValidationError("The password must be at least 5 characters long.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("The password must contain a lowercase letter.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("The password must contain an uppercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("The password must contain a digit.")
    if not re.search(r"[_@$]", password):
        raise ValidationError("The password must contain one of _ @ $")
    if confirmation is not None and password != confirmation:
        raise ValidationError("The passwords do not match.")
    return password


def validate_profile(values):
    clean = {key: (value or "").strip() for key, value in values.items()}
    required = ("phone", "country", "state", "pincode", "age", "gender", "account_type")
    if any(not clean.get(key) or clean[key] == "Select" for key in required):
        raise ValidationError("All fields are required.")
    if not (
        clean["phone"].isascii()
        and clean["phone"].isdigit()
        and len(clean["phone"]) == 10
    ):
        raise ValidationError("Enter a valid 10 digit phone number.")
    for key, label in (("pincode", "pincode"), ("age", "age")):
        if not (clean[key].isascii() and clean[key].isdigit()) or int(clean[key]) == 0:
            raise ValidationError(f"Enter a valid {label}.")
    if clean["gender"] not in GENDERS:
        raise ValidationError("Select your gender.")
    if clean["account_type"] not in ACCOUNT_TYPES:
        raise ValidationError("Select an account type.")
    return clean
