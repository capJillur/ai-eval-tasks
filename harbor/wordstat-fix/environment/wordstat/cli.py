import argparse

from .core import count_words, tokenize, top_n


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordstat")
    parser.add_argument("file")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args(argv)

    with open(args.file) as f:
        text = f.read()

    for word, count in top_n(count_words(tokenize(text)), args.top):
        print(f"{word} {count}")
    return 0
