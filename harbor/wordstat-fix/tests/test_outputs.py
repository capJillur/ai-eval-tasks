"""Hidden tests. They write their own inputs, so hardcoding the sample's output can't pass."""
import subprocess
import sys


def run(tmp_path, text, *args):
    f = tmp_path / "in.txt"
    f.write_text(text)
    return subprocess.run(
        [sys.executable, "-m", "wordstat", str(f), *args],
        cwd="/app", capture_output=True, text=True,
    )


def lines(r):
    return r.stdout.strip().splitlines()


def test_case_insensitive(tmp_path):
    r = run(tmp_path, "Apple apple APPLE banana")
    assert r.returncode == 0
    assert lines(r) == ["apple 3", "banana 1"]


def test_punctuation_stripped(tmp_path):
    r = run(tmp_path, "Hello, world! Hello.")
    assert lines(r) == ["hello 2", "world 1"]


def test_internal_apostrophe_kept_outer_quotes_dropped(tmp_path):
    r = run(tmp_path, "Don't stop. don't 'quoted' word")
    assert lines(r) == ["don't 2", "quoted 1", "stop 1", "word 1"]


def test_digits_and_mixed(tmp_path):
    r = run(tmp_path, "R2D2 r2d2 c3po")
    assert lines(r) == ["r2d2 2", "c3po 1"]


def test_alphabetical_tie_break(tmp_path):
    r = run(tmp_path, "zeta beta alpha gamma")
    assert lines(r) == ["alpha 1", "beta 1", "gamma 1", "zeta 1"]


def test_top_n_exact(tmp_path):
    r = run(tmp_path, "a a a b b c d e", "--top", "3")
    assert lines(r) == ["a 3", "b 2", "c 1"]


def test_default_top_is_ten(tmp_path):
    words = " ".join(f"w{i:02d}" for i in range(12))
    r = run(tmp_path, words)
    assert len(lines(r)) == 10


def test_top_larger_than_unique(tmp_path):
    r = run(tmp_path, "x y", "--top", "50")
    assert lines(r) == ["x 1", "y 1"]


def test_multiline(tmp_path):
    r = run(tmp_path, "One fish\ntwo fish\nRed fish\nblue FISH", "--top", "2")
    assert lines(r) == ["fish 4", "blue 1"]


def test_empty_file(tmp_path):
    r = run(tmp_path, "")
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_missing_file_exit_code_2():
    r = subprocess.run(
        [sys.executable, "-m", "wordstat", "/nonexistent/file.txt"],
        cwd="/app", capture_output=True, text=True,
    )
    assert r.returncode == 2
    assert r.stderr.strip() != ""
