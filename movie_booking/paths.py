"""Gives the folder locations the app uses for its files."""

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PACKAGE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
POSTERS_DIR = ASSETS_DIR / "posters"
MOVIES_CSV = ASSETS_DIR / "movies.csv"
SCHEMA_SQL = ASSETS_DIR / "schema.sql"

PROJECT_ROOT = PACKAGE_DIR.parent


def data_dir():
    path = Path(os.environ.get("MTB_DATA_DIR") or PROJECT_ROOT / "data")
    path.mkdir(parents=True, exist_ok=True)
    return path
