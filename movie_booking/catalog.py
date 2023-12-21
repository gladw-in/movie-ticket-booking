"""Reads the list of movies from the movies CSV file."""

import csv
from dataclasses import dataclass
from pathlib import Path

from .paths import ASSETS_DIR, MOVIES_CSV

MAX_MOVIES = 5


@dataclass(frozen=True)
class Movie:
    title: str
    poster: Path

    @property
    def has_poster(self):
        return self.poster.is_file()


def load_movies(csv_path=None, *, limit=MAX_MOVIES):
    csv_path = csv_path or MOVIES_CSV
    movies = []
    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                title = (row.get("movie_name") or "").strip()
                poster = (row.get("image_url") or "").strip().replace("\\", "/")
                if not title or not poster:
                    continue
                movies.append(Movie(title, ASSETS_DIR / poster))
                if len(movies) >= limit:
                    break
    except FileNotFoundError:
        return []
    return movies
