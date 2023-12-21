"""Checks the details typed in on the sign-up and password reset forms."""

USERNAME_MIN, USERNAME_MAX = 4, 20
PASSWORD_MIN, PASSWORD_MAX = 4, 20
PHONE_DIGITS = 10
_USERNAME_FORBIDDEN = frozenset("`~!#@$%^&*()-=+{}[]:|;'\"\\<>?,/")


class ValidationError(ValueError):
    pass


def validate_username(username):
    if not username:
        raise ValidationError("Enter a username.")
    if username.isspace() or any(ch.isspace() for ch in username):
        raise ValidationError("The username cannot contain spaces.")
    if len(username) < USERNAME_MIN:
        raise ValidationError(
            f"The username must be at least {USERNAME_MIN} characters."
        )
    if len(username) > USERNAME_MAX:
        raise ValidationError(
            f"The username must be at most {USERNAME_MAX} characters."
        )
    if any(ch in _USERNAME_FORBIDDEN for ch in username):
        raise ValidationError(
            "The username can only contain letters, digits and the symbols _ and ."
        )
    return username


def validate_phone(phone):
    if not phone:
        raise ValidationError("Enter your phone number.")
    if not (phone.isascii() and phone.isdigit()):
        raise ValidationError("The phone number must contain digits only.")
    if len(phone) != PHONE_DIGITS:
        raise ValidationError(f"The phone number must be {PHONE_DIGITS} digits.")
    return phone


def validate_new_password(password, username=None):
    if not password:
        raise ValidationError("Enter a password.")
    if any(ch.isspace() for ch in password):
        raise ValidationError("The password cannot contain spaces.")
    if username is not None and password == username:
        raise ValidationError("The password cannot be the same as the username.")
    if len(password) < PASSWORD_MIN:
        raise ValidationError(
            f"The password must be at least {PASSWORD_MIN} characters."
        )
    if len(password) > PASSWORD_MAX:
        raise ValidationError(
            f"The password must be at most {PASSWORD_MAX} characters."
        )
    return password


def validate_confirmation(password, confirmation):
    if not confirmation:
        raise ValidationError("Enter the password again to confirm it.")
    if password != confirmation:
        raise ValidationError("The passwords do not match.")
