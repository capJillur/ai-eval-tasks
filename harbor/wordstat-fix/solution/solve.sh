#!/bin/bash
set -e
cat > /app/wordstat/core.py <<'PY'
import re

_WORD = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)*")


def tokenize(text):
    return _WORD.findall(text.lower())


def count_words(tokens):
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return counts


def top_n(counts, n):
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return items[:n]
PY

cat > /app/wordstat/cli.py <<'PY'
import argparse
import sys

from .core import count_words, tokenize, top_n


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordstat")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args(argv)

    try:
        with open(args.file) as f:
            text = f.read()
    except FileNotFoundError:
        print(f"wordstat: no such file: {args.file}", file=sys.stderr)
        return 2

    for word, count in top_n(count_words(tokenize(text)), args.top):
        print(f"{word} {count}")
    return 0
PY
