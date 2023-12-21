"""Handles sign-up, log-in and password reset for customer accounts."""

import random
from dataclasses import dataclass, replace
from typing import Protocol

from . import security, validation


class AccountError(Exception):
    pass


class AccountExists(AccountError):
    pass


class InvalidCredentials(AccountError):
    pass


class IdentityMismatch(AccountError):
    pass


@dataclass(frozen=True)
class Account:
    username: str
    phone: str
    password_hash: str


class AccountRepository(Protocol):
    def get(self, username): ...

    def add(self, account):
        pass

    def set_password_hash(self, username, password_hash): ...

    def delete(self, username): ...


class AccountService:
    def __init__(self, repository):
        self._repo = repository

    def sign_up(self, username, phone, password, confirmation):
        username, phone = username.strip(), phone.strip()
        validation.validate_username(username)
        validation.validate_phone(phone)
        validation.validate_new_password(password, username)
        validation.validate_confirmation(password, confirmation)

        account = Account(username, phone, security.hash_password(password))
        self._repo.add(account)
        return account

    def log_in(self, username, password):
        username = username.strip()
        if not username:
            raise InvalidCredentials("Enter your username.")
        if not password:
            raise InvalidCredentials("Enter your password.")

        account = self._repo.get(username)
        if account is None or not security.verify_password(
            password, account.password_hash
        ):
            raise InvalidCredentials("Wrong username or password.")

        if security.needs_rehash(account.password_hash):
            upgraded = security.hash_password(password)
            self._repo.set_password_hash(account.username, upgraded)
            account = replace(account, password_hash=upgraded)
        return account

    def verify_identity(self, username, phone):
        account = self._repo.get(username.strip())
        return account is not None and account.phone.strip() == phone.strip()

    def reset_password(self, username, phone, new_password, confirmation):
        if not self.verify_identity(username, phone):
            raise IdentityMismatch(
                "The username and phone number do not match an account."
            )
        username = username.strip()
        validation.validate_new_password(new_password, username)
        validation.validate_confirmation(new_password, confirmation)
        self._repo.set_password_hash(username, security.hash_password(new_password))

    def delete_account(self, username):
        self._repo.delete(username)

    @staticmethod
    def suggest_usernames(username, count=2):
        suffixes = random.sample(range(100, 1000), count)
        base = username[: validation.USERNAME_MAX - 3]
        return [
            f"{base}{n}" if i % 2 == 0 else f"{n}{base}" for i, n in enumerate(suffixes)
        ]
