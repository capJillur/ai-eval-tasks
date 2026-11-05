from slugger import slugify


def test_basic():
    assert slugify("Hello World") == "hello-world"


def test_already_slug():
    assert slugify("abc") == "abc"


def test_underscore_becomes_hyphen():
    assert slugify("A_B") == "a-b"


def test_max_length_plain_truncation():
    assert slugify("abcdef", max_length=3) == "abc"


def test_empty_string():
    assert slugify("") == ""
