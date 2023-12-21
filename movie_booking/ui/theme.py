"""Holds the colours, fonts and widget helpers used by all screens."""

import tkinter as tk

BG = "black"
FG = "white"
MUTED = "gray"
GREEN = "#39ac56"
RED = "red"
PEACH = "#FFE5B4"
LILAC = "#e4c8e6"
GOLD = "#f2c14e"
ERROR_FG = "#ff6b6b"

FONT = ("Arial", 10)
FONT_BOLD = ("Arial", 10, "bold")
FONT_TITLE = ("Arial", 14, "bold")
FONT_ENTRY = ("Arial", 14)


def label(parent, text="", **options):
    return tk.Label(parent, text=text, **{"bg": BG, "fg": FG, "font": FONT, **options})


def field_label(parent, text, **options):
    return tk.Label(
        parent,
        text=text,
        **{"bg": PEACH, "fg": "black", "font": FONT, "width": 14, "pady": 8, **options},
    )


def button(parent, text, command=None, **options):
    return tk.Button(
        parent,
        text=text,
        command=command,
        **{
            "bg": BG,
            "fg": FG,
            "activebackground": "#333333",
            "activeforeground": FG,
            "font": FONT,
            "relief": tk.RAISED,
            "borderwidth": 2,
            "cursor": "hand2",
            **options,
        },
    )


def primary_button(parent, text, command=None, **options):
    return button(
        parent, text, command, **{"bg": RED, "activebackground": "#aa0000", **options}
    )


def entry(parent, *, show="", width=16):
    return tk.Entry(
        parent,
        show=show,
        width=width,
        font=FONT_ENTRY,
        bg=LILAC,
        fg="black",
        borderwidth=2,
    )
