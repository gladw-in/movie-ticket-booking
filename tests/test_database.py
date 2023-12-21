"""Tests for the MySQL account storage."""

from contextlib import contextmanager

import mysql.connector
import pytest

from movie_booking import database
from movie_booking.accounts import Account, AccountExists
from movie_booking.config import DbSettings


class FakeCursor:
    def __init__(self, log, row=None, fail=None):
        self.log, self.row, self.fail = log, row, fail

    def execute(self, sql, params=()):
        self.log.append((" ".join(sql.split()), params))
        if self.fail:
            raise self.fail

    def fetchone(self):
        return self.row


class FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


@pytest.fixture
def run(monkeypatch):
    def install(row=None, fail=None):
        log = []

        @contextmanager
        def fake_connect(settings, *, use_database=True):
            try:
                yield FakeConn(FakeCursor(log, row, fail))
            except mysql.connector.Error as exc:
                raise database.DatabaseError(str(exc)) from exc

        monkeypatch.setattr(database, "connect", fake_connect)
        return log

    return install


def test_schema_statements_are_split_and_comment_free():
    statements = database.schema_statements()
    assert len(statements) == 1 and statements[0].startswith(
        "CREATE TABLE IF NOT EXISTS acc"
    )
    assert "--" not in statements[0]


def test_schema_statements_handle_multiple_statements():
    assert database.schema_statements("-- c\nA;\n\nB;\n") == ["A", "B"]


def test_database_name_is_validated_before_being_interpolated():
    with pytest.raises(database.DatabaseError):
        database._quote_identifier("x`; DROP DATABASE y; --")
    assert database._quote_identifier("movie_ticketbooking") == "`movie_ticketbooking`"


def test_get_uses_bound_parameters_and_maps_the_row(run):
    log = run(row=("Abhik", "9822924582", "hash"))
    account = database.MySQLAccountRepository(DbSettings()).get("Abhik' OR '1'='1")
    assert account == Account("Abhik", "9822924582", "hash")
    sql, params = log[0]
    assert "%s" in sql and "Abhik" not in sql
    assert params == ("Abhik' OR '1'='1",)


def test_get_returns_none_when_missing(run):
    run(row=None)
    assert database.MySQLAccountRepository(DbSettings()).get("x") is None


def test_get_tolerates_null_columns(run):
    run(row=("old", None, None))
    assert database.MySQLAccountRepository(DbSettings()).get("old") == Account(
        "old", "", ""
    )


def test_add_translates_duplicate_key_errors(run):
    run(fail=mysql.connector.IntegrityError("Duplicate entry"))
    repo = database.MySQLAccountRepository(DbSettings())
    with pytest.raises(AccountExists):
        repo.add(Account("dup1", "9822924582", "h"))


def test_other_database_errors_are_not_mistaken_for_duplicates(run):
    run(fail=mysql.connector.OperationalError("server gone"))
    repo = database.MySQLAccountRepository(DbSettings())
    with pytest.raises(database.DatabaseError):
        repo.add(Account("user1", "9822924582", "h"))
