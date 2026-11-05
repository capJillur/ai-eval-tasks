def tokenize(text):
    return text.split()


def count_words(tokens):
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return counts


def top_n(counts, n):
    items = sorted(counts.items(), key=lambda kv: -kv[1])
    return items[: n - 1]
