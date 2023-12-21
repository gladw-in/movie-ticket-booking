"""Creates the main window and moves between screens."""

import tkinter as tk

from ..booking import BookingSession
from .errors import install_error_dialog


class App:
    def __init__(
        self,
        root,
        accounts,
        bank,
        movies,
    ):
        from .screens import (
            ROUTES,
        )

        self.root = root
        self.accounts = accounts
        self.bank = bank
        self.movies = movies
        self.session = None
        self._routes = ROUTES
        self._current = None
        install_error_dialog(root)

    def go(self, route, **params):
        screen = self._routes[route](self, **params)
        if self._current is not None:
            self._current.destroy()
        self._current = screen
        screen.pack(fill=tk.BOTH, expand=True)
        self.root.title(screen.title)
        self.root.geometry(f"{screen.size[0]}x{screen.size[1]}" if screen.size else "")
        return screen

    def start(self):
        self.go("login")

    def log_in(self, account):
        self.session = BookingSession(account.username)
        self.go("movies")

    def log_out(self, message=None):
        self.session = None
        self.go("login", message=message)

    def new_booking(self):
        if self.session is None:
            raise RuntimeError("no booking session: the customer is not logged in")
        self.session = BookingSession(self.session.username)
        self.go("movies")
