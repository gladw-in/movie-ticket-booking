"""Catches unexpected errors from Tk callbacks and shows them to the user."""

import tkinter as tk
import traceback
from tkinter import messagebox

from ..accounts import AccountError
from ..bank import BankError
from ..booking import BookingError
from ..validation import ValidationError

USER_ERRORS = (ValidationError, AccountError, BankError, BookingError)


def install_error_dialog(root):
    def report(exc_type, exc, tb):
        if isinstance(exc, USER_ERRORS):
            messagebox.showinfo("Notice", str(exc), parent=root)
            return
        traceback.print_exception(exc_type, exc, tb)
        messagebox.showerror(
            "Something went wrong",
            f"An unexpected error occurred:\n\n{exc}\n\nDetails were printed to the console.",
            parent=root,
        )

    root.report_callback_exception = report
