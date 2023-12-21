"""Loads and saves the MySQL connection settings."""

import json
import os
from dataclasses import asdict, dataclass, replace

from .paths import data_dir

ENV_MAP = {
    "host": "MTB_DB_HOST",
    "port": "MTB_DB_PORT",
    "user": "MTB_DB_USER",
    "password": "MTB_DB_PASSWORD",
    "database": "MTB_DB_NAME",
}


@dataclass(frozen=True)
class DbSettings:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str | None = None
    database: str = "movie_ticketbooking"

    def with_password(self, password):
        return replace(self, password=password)


def config_path():
    return data_dir() / "config.json"


def load_settings(path=None, environ=None):
    path = path or config_path()
    environ = os.environ if environ is None else environ

    values = {}
    if path.exists():
        try:
            values.update(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            pass

    for field, env_name in ENV_MAP.items():
        if env_name in environ:
            values[field] = environ[env_name]

    known = {k: v for k, v in values.items() if k in ENV_MAP}
    if "port" in known:
        try:
            known["port"] = int(known["port"])
        except (TypeError, ValueError):
            del known["port"]
    return DbSettings(**known)


def save_settings(settings, *, remember_password, path=None):
    path = path or config_path()
    payload = asdict(settings)
    if not remember_password:
        payload.pop("password", None)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
