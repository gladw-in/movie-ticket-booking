"""Fake in-memory helpers used by the tests."""

from movie_booking.accounts import Account, AccountExists


class FakeRepo:
    def __init__(self):
        self.rows = {}

    def get(self, username):
        return self.rows.get(username)

    def add(self, account):
        if account.username in self.rows:
            raise AccountExists("taken")
        self.rows[account.username] = account

    def set_password_hash(self, username, password_hash):
        old = self.rows[username]
        self.rows[username] = Account(old.username, old.phone, password_hash)

    def delete(self, username):
        self.rows.pop(username, None)
