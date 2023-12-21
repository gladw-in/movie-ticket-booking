"""Holds small reusable widgets used by the screens."""

import sys
import tkinter as tk

from . import theme


class Notice(tk.Label):
    def __init__(self, parent, **options):
        super().__init__(
            parent,
            text="",
            bg=theme.BG,
            fg=theme.FG,
            font=theme.FONT,
            wraplength=options.pop("wraplength", 320),
            justify=tk.CENTER,
            **options,
        )

    def error(self, text):
        self.config(text=text, fg=theme.ERROR_FG)

    def success(self, text):
        self.config(text=text, fg=theme.GREEN)

    def show(self, text):
        self.config(text=text, fg=theme.FG)

    def clear(self):
        self.config(text="")


class ScrollFrame(tk.Frame):
    def __init__(
        self,
        parent,
        *,
        bg=theme.BG,
        width=360,
        height=300,
    ):
        super().__init__(parent, bg=bg)
        self._canvas = tk.Canvas(
            self, bg=bg, highlightthickness=0, width=width, height=height
        )
        bar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=bar.set)
        bar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.body = tk.Frame(self._canvas, bg=bg)
        window = self._canvas.create_window((0, 0), window=self.body, anchor=tk.NW)
        self.body.bind(
            "<Configure>",
            lambda _e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.bind(
            "<Configure>", lambda e: self._canvas.itemconfigure(window, width=e.width)
        )

        self.bind("<Enter>", self._bind_wheel)
        self.bind("<Leave>", self._unbind_wheel)
        self.bind("<Destroy>", self._on_destroy)

    def _bind_wheel(self, _event=None):
        self._canvas.bind_all("<MouseWheel>", self._on_wheel)
        self._canvas.bind_all(
            "<Button-4>", lambda _e: self._canvas.yview_scroll(-1, "units")
        )
        self._canvas.bind_all(
            "<Button-5>", lambda _e: self._canvas.yview_scroll(1, "units")
        )

    def _on_destroy(self, event):
        if event.widget is self:
            self._unbind_wheel()

    def _unbind_wheel(self, _event=None):
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self._canvas.unbind_all(sequence)

    def _on_wheel(self, event):
        step = -1 * (event.delta // 120 if sys.platform != "darwin" else event.delta)
        self._canvas.yview_scroll(step, "units")

    def clear(self):
        for child in self.body.winfo_children():
            child.destroy()
        self._canvas.yview_moveto(0)
