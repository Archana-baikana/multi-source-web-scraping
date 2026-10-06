
from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "A Light in the Attic",
        "category": "",
        "price": 51.77,
        "author": "",
        "tags": [],
        "description": "",
        "scraped_at": "2026-10-06T00:00:00",
    }

    assert validate_record(record) == []


def test_invalid_price():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": "invalid",
        "rating": 3,
    }

    errors = validate_record(record)

    assert "price must be numeric" in errors


def test_invalid_rating():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "price": 10.5,
        "rating": 6,
    }

    errors = validate_record(record)

    assert "rating must be between 1 and 5" in errors