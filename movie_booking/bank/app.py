"""Shows the bank simulator window."""

import argparse
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, ttk

from ..paths import IMG_DIR, data_dir
from ..ui.errors import install_error_dialog
from ..ui.images import photo, set_window_icon
from ..validation import ValidationError
from . import rules
from .store import PROFILE_FIELDS, BankError, BankStore, import_legacy_files

WINDOW = (600, 440)
BG = "white"
FONT = ("Arial", 11)


@dataclass(frozen=True)
class Field:
    key: str
    caption: str
    secret: bool = False
    choices: tuple[str, ...] = ()
    initial: str = ""


class FormDialog(tk.Toplevel):
    def __init__(
        self,
        parent,
        title,
        fields,
        submit_text,
        on_submit,
        extra=(),
    ):
        super().__init__(parent, bg=BG, padx=20, pady=16)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self._on_submit = on_submit
        self._fields = fields
        self._inputs = {}

        for row, field in enumerate(fields):
            tk.Label(self, text=field.caption, bg=BG, font=FONT, anchor=tk.W).grid(
                row=row, column=0, sticky=tk.W, pady=4
            )
            if field.choices:
                widget = ttk.Combobox(
                    self, values=field.choices, state="readonly", width=24, font=FONT
                )
                widget.set(field.initial or "Select")
            else:
                widget = tk.Entry(
                    self, show="*" if field.secret else "", width=26, font=FONT
                )
                widget.insert(0, field.initial)
            widget.grid(row=row, column=1, padx=(12, 0), pady=4)
            self._inputs[field.key] = widget

        self.notice = tk.Label(
            self, text="", bg=BG, fg="#c0392b", font=("Arial", 10), wraplength=340
        )
        self.notice.grid(row=len(fields), column=0, columnspan=2, pady=6)
        buttons = tk.Frame(self, bg=BG)
        buttons.grid(row=len(fields) + 1, column=0, columnspan=2)
        tk.Button(
            buttons,
            text=submit_text,
            command=self.submit,
            bg="black",
            fg="white",
            width=14,
        ).pack(side=tk.LEFT, padx=4)
        for text, action in extra:
            tk.Button(buttons, text=text, command=action, width=14).pack(
                side=tk.LEFT, padx=4
            )
        tk.Button(buttons, text="Cancel", command=self.destroy, width=10).pack(
            side=tk.LEFT, padx=4
        )

        self.bind("<Return>", lambda _e: self.submit())
        self.bind("<Escape>", lambda _e: self.destroy())
        first = next(iter(self._inputs.values()))
        first.focus_set()
        self.grab_set()

    def submit(self):
        values = {
            field.key: (
                self._inputs[field.key].get()
                if field.secret
                else self._inputs[field.key].get().strip()
            )
            for field in self._fields
        }
        try:
            self._on_submit(values)
        except (ValidationError, BankError) as exc:
            self.notice.config(text=str(exc))
            return
        self.destroy()


class BankApp:
    def __init__(self, root, store):
        self.root, self.store = root, store
        self.user = None
        root.title("Bank")
        root.geometry(f"{WINDOW[0]}x{WINDOW[1]}")
        root.resizable(False, False)
        install_error_dialog(root)
        set_window_icon(root)

        backdrop = photo(root, IMG_DIR / "background_image.png", WINDOW)
        if backdrop is not None:
            tk.Label(root, image=backdrop).place(x=0, y=0, relwidth=1, relheight=1)
        logo = photo(root, IMG_DIR / "logo.png", (190, 112))
        if logo is not None:
            tk.Label(root, image=logo, bg=BG).pack(pady=(20, 18))

        for text, action in (
            ("Admin login", self.admin),
            ("Register", self.register),
            ("Log in", self.log_in),
            ("Exit", root.destroy),
        ):
            tk.Button(
                root,
                text=text,
                command=action,
                width=22,
                bg="black",
                fg="white",
                font=FONT,
                pady=4,
            ).pack(pady=5)

    def show_login_state(self):
        self.root.title(f"Bank - logged in as {self.user}" if self.user else "Bank")

    def register(self):
        def submit(v):
            self.store.register(v["name"], v["password"], v["confirm"])
            messagebox.showinfo(
                "Registered", "Account created. You can log in now.", parent=self.root
            )

        FormDialog(
            self.root,
            "Register",
            [
                Field("name", "Account name"),
                Field("password", "Password", secret=True),
                Field("confirm", "Confirm password", secret=True),
            ],
            "Register",
            submit,
        )

    def _user(self):
        if self.user is None:
            raise BankError("Please log in first.")
        return self.user

    def log_in(self):
        if self.user is not None:
            messagebox.showinfo(
                "Already logged in",
                f"{self.user} is logged in. Log out first.",
                parent=self.root,
            )
            return

        def submit(v):
            self.user = self.store.authenticate(v["name"], v["password"])
            self.store.log_event(self.user, "Logged in")
            self.show_login_state()
            self.account_window()

        FormDialog(
            self.root,
            "Log in",
            [Field("name", "Account name"), Field("password", "Password", secret=True)],
            "Log in",
            submit,
            extra=[("Forgot password", self.forgot_password)],
        )

    def forgot_password(self):
        def submit(v):
            self.store.reset_password(
                v["name"], v["phone"], v["password"], v["confirm"]
            )
            messagebox.showinfo(
                "Password changed", "Your password was changed.", parent=self.root
            )

        FormDialog(
            self.root,
            "Reset password",
            [
                Field("name", "Account name"),
                Field("phone", "Phone (from personal info)"),
                Field("password", "New password", secret=True),
                Field("confirm", "Confirm password", secret=True),
            ],
            "Reset",
            submit,
        )

    def account_window(self):
        window = tk.Toplevel(self.root, bg=BG, padx=30, pady=20)
        window.title(f"Account - {self.user}")
        tk.Label(
            window, text=f"Hello, {self.user}", bg=BG, font=("Arial", 13, "bold")
        ).pack(pady=(0, 10))
        for text, action in (
            ("Balance", self.show_balance),
            ("Deposit", lambda: self.money("Deposit")),
            ("Withdraw", lambda: self.money("Withdraw")),
            ("Transactions", self.show_history),
            ("Personal info", self.personal_info),
        ):
            tk.Button(
                window,
                text=text,
                command=action,
                width=22,
                bg="black",
                fg="white",
                font=FONT,
            ).pack(pady=4)

        def log_out():
            if self.user is not None:
                self.store.log_event(self.user, "Logged out")
            self.user = None
            self.show_login_state()
            window.destroy()

        tk.Button(window, text="Log out", command=log_out, width=22, font=FONT).pack(
            pady=(10, 0)
        )
        window.protocol("WM_DELETE_WINDOW", log_out)

    def show_balance(self):
        messagebox.showinfo(
            "Balance",
            f"Your balance is {rules.format_money(self.store.balance(self._user()))}",
        )

    def money(self, kind):
        def submit(v):
            cents = rules.parse_amount(v["amount"])
            balance = (
                self.store.deposit(self._user(), cents)
                if kind == "Deposit"
                else self.store.withdraw(self._user(), cents)
            )
            messagebox.showinfo(
                kind, f"Done. New balance: {rules.format_money(balance)}"
            )

        FormDialog(self.root, kind, [Field("amount", "Amount (Rs)")], kind, submit)

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("Transactions")
        text = tk.Text(window, width=90, height=18, font=("Courier", 10))
        text.pack(padx=10, pady=10)
        for tx in self.store.history(self._user()):
            text.insert(tk.END, tx.describe() + "\n")
        text.config(state=tk.DISABLED)

    def personal_info(self):
        current = self.store.get_profile(self._user()) or {}

        def submit(v):
            self.store.save_profile(self._user(), v)
            messagebox.showinfo("Saved", "Your personal info was saved.")

        captions = {
            "phone": "Phone number",
            "country": "Country",
            "state": "State",
            "pincode": "Pincode",
            "age": "Age",
            "gender": "Gender",
            "account_type": "Account type",
        }
        choices = {"gender": rules.GENDERS, "account_type": rules.ACCOUNT_TYPES}
        FormDialog(
            self.root,
            "Personal info",
            [
                Field(
                    k,
                    captions[k],
                    choices=choices.get(k, ()),
                    initial=current.get(k, ""),
                )
                for k in PROFILE_FIELDS
            ],
            "Save",
            submit,
        )

    def admin(self):
        if not self.store.has_admin():

            def create(v):
                self.store.set_admin_password(v["password"], v["confirm"])
                messagebox.showinfo(
                    "Admin",
                    "Admin password set. Log in again to continue.",
                    parent=self.root,
                )

            FormDialog(
                self.root,
                "Create admin password",
                [
                    Field("password", "New admin password", secret=True),
                    Field("confirm", "Confirm", secret=True),
                ],
                "Create",
                create,
            )
            return

        def submit(v):
            if not self.store.verify_admin(v["password"]):
                raise BankError("Wrong admin password.")
            self.accounts_window()

        FormDialog(
            self.root,
            "Admin login",
            [Field("password", "Admin password", secret=True)],
            "Log in",
            submit,
        )

    def accounts_window(self):
        window = tk.Toplevel(self.root)
        window.title("All accounts")
        table = ttk.Treeview(
            window, columns=("name", "balance", "created"), show="headings", height=14
        )
        for column, title, width in (
            ("name", "Account", 160),
            ("balance", "Balance", 120),
            ("created", "Created", 160),
        ):
            table.heading(column, text=title)
            table.column(column, width=width)
        for account in self.store.list_accounts():
            table.insert(
                "",
                tk.END,
                values=(
                    account.name,
                    rules.format_money(account.balance_cents),
                    account.created_at,
                ),
            )
        table.pack(padx=10, pady=10)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m movie_booking.bank", description="Bank simulator."
    )
    parser.add_argument(
        "--import-legacy",
        metavar="DIR",
        help="import accounts from the old file-based bank stored in DIR, then exit",
    )
    args = parser.parse_args(argv)

    store = BankStore(data_dir() / "bank.sqlite3")
    if args.import_legacy:
        names = import_legacy_files(store, args.import_legacy)
        print(f"Imported {len(names)} account(s): {', '.join(names) or 'none'}")
        return
    root = tk.Tk()
    BankApp(root, store)
    root.mainloop()


if __name__ == "__main__":
    main()
