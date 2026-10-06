
from processing.cleaning import clean_text, clean_price, clean_tags


def test_clean_text():
    assert clean_text("  Hello   World  ") == "Hello World"


def test_clean_price():
    assert clean_price("Â£51.77") == "£51.77"


def test_clean_tags():
    assert clean_tags(["  python ", " web "]) == ["python", "web"]