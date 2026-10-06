
from processing.validation import validate_record


def test_valid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "A Light in the Attic",
        "category": "",
        "price": "£51.77",
        "author": "",
        "tags": [],
        "description": "",
        "scraped_at": "2026-10-06T00:00:00",
    }

    assert validate_record(record) == []


def test_invalid_record():
    record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "",
    }

    errors = validate_record(record)

    assert len(errors) > 0