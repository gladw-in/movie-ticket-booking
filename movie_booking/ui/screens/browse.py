"""Screen to pick a movie and a theatre."""

import tkinter as tk
from tkinter import messagebox

from ...seating import THEATRES
from .. import theme
from ..base import Screen
from ..images import photo

POSTER_SIZE = (225, 285)


class MoviesScreen(Screen):
    title = "BookMyShow.com"
    size = (390, 520)

    def build(self):
        self.index = 0
        movies = self.app.movies

        tk.Label(
            self,
            text="BookMyShow.com",
            bg="white",
            fg="black",
            font=theme.FONT_TITLE,
            pady=8,
        ).pack(fill=tk.X)
        theme.label(
            self, f"Welcome, {self.session.username}", font=theme.FONT_BOLD
        ).pack(pady=(8, 4))

        if not movies:
            theme.label(
                self, "No movies are on right now.\nCheck back later!", pady=40
            ).pack()
            self._footer()
            return

        stage = tk.Frame(self, bg=theme.BG)
        stage.pack(pady=4)
        self.back_button = theme.button(stage, "<<", lambda: self.step(-1), width=3)
        self.back_button.grid(row=0, column=0, padx=4)
        self.poster = tk.Label(
            stage,
            bg="gray",
            width=POSTER_SIZE[0],
            height=POSTER_SIZE[1],
            compound=tk.CENTER,
        )
        self.poster.grid(row=0, column=1)
        self.forward_button = theme.button(stage, ">>", lambda: self.step(1), width=3)
        self.forward_button.grid(row=0, column=2, padx=4)

        self.book_button = theme.button(self, "", self.book, width=26, pady=4)
        self.book_button.pack(pady=10)
        self._footer()
        self.refresh()

    def _footer(self):
        row = tk.Frame(self, bg=theme.BG)
        row.pack(side=tk.BOTTOM, pady=10)
        theme.button(row, "Log out", lambda: self.app.log_out(), width=12).grid(
            row=0, column=0, padx=6
        )
        theme.button(
            row, "Delete account", self.delete_account, width=14, fg="#ff8080"
        ).grid(row=0, column=1, padx=6)

    def step(self, delta):
        self.index = max(0, min(len(self.app.movies) - 1, self.index + delta))
        self.refresh()

    def refresh(self):
        movie = self.app.movies[self.index]
        image = photo(self, movie.poster, POSTER_SIZE)
        if image is not None:
            self.poster.config(
                image=image, text="", width=POSTER_SIZE[0], height=POSTER_SIZE[1]
            )
            self.poster.image = image
        else:
            self.poster.config(
                image="", text="poster\nunavailable", fg="white", width=30, height=15
            )
        self.book_button.config(text=f"{movie.title}\n---- click to book ----")
        self.back_button.config(state=tk.DISABLED if self.index == 0 else tk.NORMAL)
        self.forward_button.config(
            state=tk.DISABLED if self.index == len(self.app.movies) - 1 else tk.NORMAL
        )

    def book(self):
        self.session.movie = self.app.movies[self.index]
        self.app.go("theatre")

    def delete_account(self):
        if not messagebox.askyesno(
            "Delete account", "Do you really want to delete your account?", parent=self
        ):
            return
        username = self.session.username
        error = self.attempt(lambda: self.app.accounts.delete_account(username))
        if error is None:
            self.app.log_out("Your account was deleted.")
        else:
            messagebox.showerror("Delete account", error, parent=self)


class TheatreScreen(Screen):
    title = "Theatre"
    size = (330, 260)

    def build(self):
        theme.label(self, "CHOOSE YOUR THEATRE!", font=theme.FONT_BOLD, pady=18).pack()
        style = {"INOX": dict(fg="#6fa8ff"), "PVR": dict(fg="yellow", bg="gray")}
        for theatre in THEATRES:
            theme.button(
                self,
                theatre.name,
                lambda t=theatre: self.choose(t),
                width=14,
                font=("Arial", 11, "bold"),
                **style.get(theatre.name, {}),
            ).pack(pady=6)
        theme.button(self, "Back", lambda: self.app.go("movies"), width=14).pack(
            pady=(14, 0)
        )

    def choose(self, theatre):
        self.session.choose_theatre(theatre)
        self.app.go("seats")
