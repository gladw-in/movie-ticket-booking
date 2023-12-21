"""Gets a working MySQL connection when the app starts."""

from dataclasses import replace

from .config import save_settings
from .database import DatabaseError, ensure_schema


def connect_or_prompt(
    settings,
    *,
    ask_password,
    show_error,
    ask_remember,
    ensure=ensure_schema,
    save=save_settings,
    attempts=3,
):
    typed = False
    for _ in range(attempts):
        if settings.password is None:
            password = ask_password(settings)
            if password is None:
                return None
            settings, typed = settings.with_password(password), True
        try:
            ensure(settings)
        except DatabaseError as exc:
            show_error(str(exc))
            settings = replace(settings, password=None)
            continue
        if typed:
            save(settings, remember_password=ask_remember())
        return settings
    return None
