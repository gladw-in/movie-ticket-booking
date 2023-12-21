"""Shared test setup that makes password hashing fast."""

import pytest

from movie_booking import security


@pytest.fixture(autouse=True)
def fast_hashing(monkeypatch):
    monkeypatch.setattr(security, "ITERATIONS", 1_000)
