import re


def slugify(text, max_length=None):
    """Turn arbitrary text into a URL slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", "-", text)
    if max_length is not None:
        text = text[:max_length]
    return text
