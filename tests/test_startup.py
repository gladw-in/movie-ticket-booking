"""Tests for getting a MySQL connection at start-up."""

from movie_booking.config import DbSettings
from movie_booking.database import DatabaseError
from movie_booking.startup import connect_or_prompt


class Harness:
    def __init__(self, passwords=(), working="right", remember=False):
        self.passwords, self.working, self.remember_answer = (
            list(passwords),
            working,
            remember,
        )
        self.errors, self.saved, self.asked = [], [], 0

    def ask_password(self, _settings):
        self.asked += 1
        return self.passwords.pop(0) if self.passwords else None

    def ensure(self, settings):
        if settings.password != self.working:
            raise DatabaseError("Access denied")

    def save(self, settings, *, remember_password):
        self.saved.append((settings.password, remember_password))

    def run(self, settings=None, **kw):
        settings = settings or DbSettings()
        return connect_or_prompt(
            settings,
            ask_password=self.ask_password,
            show_error=self.errors.append,
            ask_remember=lambda: self.remember_answer,
            ensure=self.ensure,
            save=self.save,
            **kw,
        )


def test_configured_password_is_used_without_prompting_or_saving():
    h = Harness()
    result = h.run(DbSettings(password="right"))
    assert result.password == "right" and h.asked == 0 and h.saved == []


def test_prompts_when_no_password_and_saves_the_choice():
    h = Harness(["right"], remember=True)
    assert h.run().password == "right"
    assert h.saved == [("right", True)]


def test_wrong_password_shows_the_error_and_asks_again():
    h = Harness(["wrong", "right"])
    assert h.run().password == "right"
    assert h.errors == ["Access denied"] and h.asked == 2


def test_rejected_configured_password_falls_back_to_asking():
    h = Harness(["right"])
    assert h.run(DbSettings(password="stale")).password == "right"
    assert h.errors == ["Access denied"]


def test_cancelling_returns_none():
    assert Harness([]).run() is None


def test_gives_up_after_too_many_failures():
    h = Harness(["a", "b", "c", "d"])
    assert h.run(attempts=3) is None and len(h.errors) == 3
