"""Tests for loading the movie list."""

from movie_booking.catalog import MAX_MOVIES, load_movies
from movie_booking.paths import ASSETS_DIR


def write_csv(tmp_path, body):
    path = tmp_path / "movies.csv"
    path.write_text("slno,movie_name,image_url\n" + body, encoding="utf-8")
    return path


def test_bundled_catalog_loads_and_all_posters_exist():
    movies = load_movies()
    assert [m.title for m in movies] == [
        "batman",
        "mission impossible",
        "avatar",
        "kantara",
    ]
    assert all(m.has_poster for m in movies)


def test_windows_style_paths_are_normalised(tmp_path):
    path = write_csv(tmp_path, '1,batman,"posters\\batman.jpg"\n')
    assert load_movies(path)[0].poster == ASSETS_DIR / "posters" / "batman.jpg"


def test_limit_and_blank_rows(tmp_path):
    body = "".join(f"{i},m{i},posters/batman.jpg\n" for i in range(9)) + ",,\n"
    assert len(load_movies(write_csv(tmp_path, body))) == MAX_MOVIES
    assert len(load_movies(write_csv(tmp_path, body), limit=2)) == 2
    assert load_movies(write_csv(tmp_path, ",,\n1,,x.jpg\n")) == []


def test_missing_file_gives_an_empty_catalog(tmp_path):
    assert load_movies(tmp_path / "nope.csv") == []


def test_missing_poster_is_reported_not_fatal(tmp_path):
    movie = load_movies(write_csv(tmp_path, "1,ghost,posters/ghost.jpg\n"))[0]
    assert not movie.has_poster


def test_csv_saved_with_a_byte_order_mark_still_loads(tmp_path):
    path = tmp_path / "movies.csv"
    path.write_bytes(
        "\ufeffmovie_name,image_url\nbatman,posters/batman.jpg\n".encode("utf-8")
    )
    assert [m.title for m in load_movies(path)] == ["batman"]
