"""Starts the movie booking app when you run the package."""

from .accounts import AccountService
from .bank import BankStore
from .catalog import load_movies
from .config import load_settings
from .database import MySQLAccountRepository
from .paths import data_dir
from .startup import connect_or_prompt


def main():
    import tkinter as tk
    from tkinter import messagebox, simpledialog

    from .ui.app import App
    from .ui.images import set_window_icon

    root = tk.Tk()
    root.withdraw()
    settings = connect_or_prompt(
        load_settings(),
        ask_password=lambda s: simpledialog.askstring(
            "MySQL password", f"Password for {s.user}@{s.host}:", show="*", parent=root
        ),
        show_error=lambda message: messagebox.showerror(
            "Cannot connect to MySQL", message, parent=root
        ),
        ask_remember=lambda: messagebox.askyesno(
            "Remember password?",
            "Save the MySQL password on this computer so you aren't asked next time?",
            parent=root,
        ),
    )
    if settings is None:
        root.destroy()
        return

    set_window_icon(root)
    bank = BankStore(data_dir() / "bank.sqlite3")
    app = App(
        root, AccountService(MySQLAccountRepository(settings)), bank, load_movies()
    )
    root.deiconify()
    app.start()
    root.mainloop()


if __name__ == "__main__":
    main()
