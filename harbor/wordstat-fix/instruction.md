The Python package in `/app/wordstat` is a small CLI that counts word frequencies, but it
produces wrong output. Fix it so it behaves exactly as described below.

Usage:

    python -m wordstat <file> [--top N]

Behavior:

1. Words are case-insensitive: `Apple` and `apple` are the same word, printed in lowercase.
2. Punctuation is not part of a word. A word is a run of letters/digits, and may contain
   internal apostrophes (`don't` is one word). Leading/trailing quotes or punctuation are dropped.
3. Print one line per word in the format `<word> <count>`.
4. Sort by count descending; break ties alphabetically (A to Z).
5. Print at most N lines (default N = 10). `--top 3` prints exactly 3 lines when at least
   3 distinct words exist.
6. An empty file prints nothing and exits with code 0.
7. If the file does not exist, print a message to stderr and exit with code 2.

Example (`/app/sample.txt` is provided):

    $ python -m wordstat /app/sample.txt --top 2
    the 3
    fox 2

Do not change the command-line interface.
