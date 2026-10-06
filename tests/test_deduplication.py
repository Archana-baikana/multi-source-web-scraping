
from processing.deduplication import deduplicate_records


def test_deduplicate_records():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "Book A",
            "author": "",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Book A",
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