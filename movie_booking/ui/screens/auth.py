"""Screens for log in, sign up and password reset."""

import tkinter as tk

from ...accounts import AccountExists
from .. import theme
from ..base import Screen
from ..widgets import Notice


def _form_row(parent, row, caption, *, secret=False):
    theme.field_label(parent, caption).grid(
        row=row, column=0, padx=(16, 6), pady=6, sticky=tk.E
    )
    box = theme.entry(parent, show="*" if secret else "")
    box.grid(row=row, column=1, padx=(0, 16), pady=6)
    return box


def _show_password_toggle(parent, *entries):
    shown = tk.BooleanVar(value=False)

    def apply():
        for box in entries:
            box.config(show="" if shown.get() else "*")

    return tk.Checkbutton(
        parent,
        text="show password",
        variable=shown,
        command=apply,
        bg=theme.BG,
        fg=theme.FG,
        selectcolor=theme.BG,
        activebackground=theme.BG,
        activeforeground=theme.FG,
        font=theme.FONT,
    )


class LoginScreen(Screen):
    title = "Log in"
    size = (420, 400)

    def build(self, message=None):
        tk.Label(
            self,
            text="LOG IN",
            bg=theme.PEACH,
            fg="black",
            font=theme.FONT_BOLD,
            width=16,
            pady=8,
        ).pack(pady=(24, 12))
        form = tk.Frame(self, bg=theme.BG)
        form.pack()
        self.username = _form_row(form, 0, "Username")
        self.password = _form_row(form, 1, "Password", secret=True)

        _show_password_toggle(self, self.password).pack(
            anchor=tk.W, padx=40, pady=(4, 0)
        )
        forgot = theme.label(self, "forgot password?", fg="#6fa8ff", cursor="hand2")
        forgot.pack(anchor=tk.W, padx=44)
        forgot.bind("<Button-1>", lambda _e: self.app.go("forgot"))

        theme.button(
            self, "log in", self.submit, width=14, bg="lightgray", fg="black"
        ).pack(pady=(12, 4))
        theme.label(self, "did not sign up yet?", font=("Arial", 8)).pack()
        theme.button(
            self,
            "sign up",
            lambda: self.app.go("signup"),
            width=14,
            bg="lightgray",
            fg="black",
        ).pack(pady=4)

        self.notice = Notice(self)
        self.notice.pack(pady=8)
        if message:
            self.notice.success(message)

        self.username.focus_set()
        for box in (self.username, self.password):
            box.bind("<Return>", lambda _e: self.submit())

    def submit(self):
        def attempt():
            account = self.app.accounts.log_in(self.username.get(), self.password.get())
            self.app.log_in(account)

        self.guard(self.notice, attempt)


class SignupScreen(Screen):
    title = "Sign up"
    size = (420, 520)

    def build(self):
        tk.Label(
            self,
            text="SIGN UP",
            bg=theme.PEACH,
            fg="black",
            font=theme.FONT_BOLD,
            width=16,
            pady=8,
        ).pack(pady=(20, 8))
        form = tk.Frame(self, bg=theme.BG)
        form.pack()
        self.username = _form_row(form, 0, "Username")
        self.phone = _form_row(form, 1, "Phone number")
        self.password = _form_row(form, 2, "Password", secret=True)
        self.confirm = _form_row(form, 3, "Confirm\npassword", secret=True)

        _show_password_toggle(self, self.password, self.confirm).pack(
            anchor=tk.W, padx=40, pady=(4, 0)
        )

        self.human = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self,
            text="I am not a robot",
            variable=self.human,
            command=self._sync_button,
            bg=theme.BG,
            fg=theme.FG,
            selectcolor=theme.BG,
            activebackground=theme.BG,
            activeforeground=theme.FG,
            font=theme.FONT,
        ).pack(anchor=tk.W, padx=40, pady=4)

        self.submit_button = theme.button(
            self,
            "sign up",
            self.submit,
            width=14,
            bg="lightgray",
            fg="black",
            state=tk.DISABLED,
        )
        self.submit_button.pack(pady=(8, 4))
        theme.button(
            self, "back to log in", lambda: self.app.go("login"), width=14
        ).pack(pady=4)

        self.notice = Notice(self, wraplength=360)
        self.notice.pack(pady=8)
        self.username.focus_set()

    def _sync_button(self):
        self.submit_button.config(state=tk.NORMAL if self.human.get() else tk.DISABLED)

    def submit(self):
        username = self.username.get().strip()

        def attempt():
            try:
                self.app.accounts.sign_up(
                    username, self.phone.get(), self.password.get(), self.confirm.get()
                )
            except AccountExists:
                options = " or ".join(self.app.accounts.suggest_usernames(username))
                raise AccountExists(
                    f"That username is already taken. Try {options}."
                ) from None

        if self.guard(self.notice, attempt):
            self.app.go("login", message="Account created. You can log in now.")
        else:
            self.human.set(False)
            self._sync_button()


class ForgotPasswordScreen(Screen):
    title = "Forgot password"
    size = (420, 400)

    def build(self):
        tk.Label(
            self,
            text="FORGOT PASSWORD",
            bg=theme.PEACH,
            fg="black",
            font=theme.FONT_BOLD,
            width=20,
            pady=8,
        ).pack(pady=(24, 12))
        self.identity = tk.Frame(self, bg=theme.BG)
        self.identity.pack()
        self.username = _form_row(self.identity, 0, "Username")
        self.phone = _form_row(self.identity, 1, "Phone number")
        self.verify_button = theme.button(
            self, "verify", self.verify, width=16, bg="lightgray", fg="black"
        )
        self.verify_button.pack(pady=10)

        self.new_password_frame = tk.Frame(self, bg=theme.BG)
        self.new_password = _form_row(
            self.new_password_frame, 0, "New password", secret=True
        )
        self.confirm = _form_row(
            self.new_password_frame, 1, "Confirm\npassword", secret=True
        )
        self.reset_button = theme.button(
            self, "reset password", self.reset, width=16, bg="lightgray", fg="black"
        )

        theme.button(
            self, "back to log in", lambda: self.app.go("login"), width=16
        ).pack(pady=4, side=tk.BOTTOM)
        self.notice = Notice(self, wraplength=360)
        self.notice.pack(side=tk.BOTTOM, pady=8)
        self.username.focus_set()

    def verify(self):
        matched = False

        def attempt():
            nonlocal matched
            matched = self.app.accounts.verify_identity(
                self.username.get(), self.phone.get()
            )

        if not self.guard(self.notice, attempt):
            return
        if not matched:
            self.notice.error("The username and phone number do not match an account.")
            return
        for box in (self.username, self.phone):
            box.config(state=tk.DISABLED)
        self.verify_button.pack_forget()
        self.new_password_frame.pack()
        self.reset_button.pack(pady=10)
        self.new_password.focus_set()
        self.notice.success("Identity confirmed. Choose a new password.")

    def reset(self):
        def attempt():
            self.app.accounts.reset_password(
                self.username.get(),
                self.phone.get(),
                self.new_password.get(),
                self.confirm.get(),
            )

        if self.guard(self.notice, attempt):
            self.app.go("login", message="Password changed. Please log in.")
