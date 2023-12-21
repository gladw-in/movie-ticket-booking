"""Tests for loading and saving connection settings."""

import json

from movie_booking.config import DbSettings, load_settings, save_settings


def test_defaults_when_nothing_is_configured(tmp_path):
    settings = load_settings(tmp_path / "missing.json", environ={})
    assert settings == DbSettings() and settings.password is None


def test_environment_overrides_file(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"host": "filehost", "user": "fileuser", "port": 3307}))
    settings = load_settings(
        path, environ={"MTB_DB_HOST": "envhost", "MTB_DB_PASSWORD": "pw"}
    )
    assert (settings.host, settings.user, settings.port, settings.password) == (
        "envhost",
        "fileuser",
        3307,
        "pw",
    )


def test_password_is_only_saved_on_request(tmp_path):
    path = tmp_path / "config.json"
    settings = DbSettings(password="s3cret")
    save_settings(settings, remember_password=False, path=path)
    assert "password" not in json.loads(path.read_text())
    save_settings(settings, remember_password=True, path=path)
    assert json.loads(path.read_text())["password"] == "s3cret"


def test_corrupt_file_and_bad_port_fall_back_to_defaults(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("{not json")
    assert load_settings(path, environ={}) == DbSettings()
    assert load_settings(path, environ={"MTB_DB_PORT": "abc"}).port == 3306
