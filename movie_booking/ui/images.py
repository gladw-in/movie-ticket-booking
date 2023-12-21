"""Loads images and the window icon for Tk."""

from PIL import Image, ImageOps, ImageTk


def photo(widget, path, size):
    root = widget.winfo_toplevel()
    cache = root.__dict__.setdefault("_photo_cache", {})
    key = (str(path), size)
    if key not in cache:
        try:
            with Image.open(path) as source:
                cache[key] = ImageTk.PhotoImage(
                    ImageOps.fit(source.convert("RGBA"), size), master=root
                )
        except (OSError, ValueError):
            return None
    return cache[key]


def set_window_icon(root):
    from ..paths import IMG_DIR

    icon = photo(root, IMG_DIR / "logo.png", (64, 64))
    if icon is not None:
        root.iconphoto(True, icon)
