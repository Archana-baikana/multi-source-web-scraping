
from processing.deduplication import deduplicate_records


def test_deduplicate_books_with_case_and_spacing():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Book A",
            "author": "",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "  BOOK   A  ",
            "author": "",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Book B",
            "author": "",
        },
    ]

    result = deduplicate_records(records)

    assert len(result) == 2


def test_deduplicate_quotes():
    records = [
        {
            "source": "Quotes to Scrape",
            "name_or_title": "The world is beautiful",
            "author": "Albert",
        },
        {
            "source": "Quotes to Scrape",
            "name_or_title": "The world is beautiful",
            "author": "Albert",
        },
        {
            "source": "Quotes to Scrape",
            "name_or_title": "Another quote",
            "author": "John",
        },
    ]

    result = deduplicate_records(records)

    assert len(result) == 2