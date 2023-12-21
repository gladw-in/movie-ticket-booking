"""Gives every screen a common base class and shared error handling."""

import sys
import tkinter as tk
from typing import TYPE_CHECKING

from ..database import DatabaseError
from . import theme
from .errors import USER_ERRORS

if TYPE_CHECKING:
    from .app import App


class Screen(tk.Frame):
    title = "BookMyShow.com"
    size = None

    def __init__(self, app, **params):
        super().__init__(app.root, bg=theme.BG)
        self.app = app
        self.build(**params)

    @property
    def session(self):
        if self.app.session is None:
            raise RuntimeError("no booking session: the customer is not logged in")
        return self.app.session

    def build(self):
        raise NotImplementedError

    def attempt(self, action):
        try:
            action()
            return None
        except USER_ERRORS as exc:
            return str(exc)
        except DatabaseError as exc:
            print(exc, file=sys.stderr)
            return "The database is unavailable. Check that MySQL is running and try again."

    def guard(self, notice, action):
        error = self.attempt(action)
        if error is not None:
            notice.error(error)
        return error is None
