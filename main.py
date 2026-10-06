
import csv
import json
import logging
import os
import time
from collections import Counter
from datetime import datetime, timezone

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_record
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


OUTPUT_DIR = "output"
LOG_DIR = "logs"

CSV_PATH = os.path.join(OUTPUT_DIR, "final_dataset.csv")
JSON_PATH = os.path.join(OUTPUT_DIR, "summary_report.json")
LOG_PATH = os.path.join(LOG_DIR, "scraper.log")

COLUMNS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_PATH,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def prepare_record(record):
    """Add missing common-schema fields."""
    record = record.copy()

    record.setdefault("category", "")
    record.setdefault("price", None)
    record.setdefault("rating", None)
    record.setdefault("author", "")
    record.setdefault("tags", [])
    record.setdefault("description", "")
    record.setdefault(
        "scraped_at",
        datetime.now(timezone.utc).isoformat()
    )

    return record


def prepare_for_csv(record):
    """Convert cleaned record into CSV-friendly values."""
    record = record.copy()

    tags = record.get("tags", [])

    if isinstance(tags, list):
        record["tags"] = ";".join(tags)

    return record


def get_rejection_reasons(invalid_records):
    """Count validation rejection reasons."""
    reasons = Counter()

    for item in invalid_records:
        for error in item.get("errors", []):
            reasons[error] += 1

    return dict(reasons)


def run_source(scraper, source_name):
    """Run one scraper without stopping the other source."""
    try:
        logger.info("%s scraping started", source_name)

        records = scraper()

        logger.info(
            "%s scraping completed: %d records",
            source_name,
            len(records)
        )

        return records

    except Exception as error:
        logger.error(
            "%s scraping failed: %s",
            source_name,
            error
        )

        return []


def main():
    start_time = datetime.now(timezone.utc)

    logger.info("Scraping pipeline started")

    # -------------------------------------------------
    # 1. SCRAPE
    # -------------------------------------------------

    books = run_source(
        scrape_books,
        "Books to Scrape"
    )

    quotes = run_source(
        scrape_quotes,
        "Quotes to Scrape"
    )

    raw_records = books + quotes

    raw_counts = {
        "Books to Scrape": len(books),
        "Quotes to Scrape": len(quotes),
    }

    logger.info(
        "Total raw records: %d",
        len(raw_records)
    )

    # -------------------------------------------------
    # 2. CLEAN
    # -------------------------------------------------

    prepared_records = [
        prepare_record(record)
        for record in raw_records
    ]

    cleaned_records = [
        clean_record(record)
        for record in prepared_records
    ]

    cleaned_counts = Counter(
        record.get("source", "")
        for record in cleaned_records
    )

    logger.info(
        "Cleaning completed: %d records",
        len(cleaned_records)
    )

    # -------------------------------------------------
    # 3. VALIDATE
    # -------------------------------------------------

    valid_records, invalid_records = validate_records(
        cleaned_records
    )

    for invalid in invalid_records:
        logger.warning(
            "Rejected record: %s",
            invalid.get("errors")
        )

    rejection_reasons = get_rejection_reasons(
        invalid_records
    )

    rejected_counts = Counter(
        record.get("source", "")
        for item in invalid_records
        for record in [item.get("record", {})]
    )

    logger.info(
        "Validation completed: %d valid, %d rejected",
        len(valid_records),
        len(invalid_records)
    )

    # -------------------------------------------------
    # 4. DEDUPLICATE
    # -------------------------------------------------

    unique_records = deduplicate_records(
        valid_records
    )

    duplicates_removed = (
        len(valid_records) - len(unique_records)
    )

    logger.info(
        "Duplicates removed: %d",
        duplicates_removed
    )

    # -------------------------------------------------
    # 5. CONSOLIDATE
    # -------------------------------------------------

    final_records = [
        prepare_for_csv(record)
        for record in unique_records
    ]

    # -------------------------------------------------
    # 6. SAVE CSV
    # -------------------------------------------------

    with open(
        CSV_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS
        )

        writer.writeheader()

        for record in final_records:
            writer.writerow({
                column: record.get(column, "")
                for column in COLUMNS
            })

    logger.info(
        "CSV saved: %s",
        CSV_PATH
    )

    # -------------------------------------------------
    # 7. SUMMARY
    # -------------------------------------------------

    end_time = datetime.now(timezone.utc)

    duration_seconds = (
        end_time - start_time
    ).total_seconds()

    final_counts = Counter(
        record.get("source", "")
        for record in unique_records
    )

    summary = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": duration_seconds,

        "raw_records": {
            "Books to Scrape": raw_counts.get(
                "Books to Scrape", 0
            ),
            "Quotes to Scrape": raw_counts.get(
                "Quotes to Scrape", 0
            ),
            "total": len(raw_records),
        },

        "records_after_cleaning": {
            "Books to Scrape": cleaned_counts.get(
                "Books to Scrape", 0
            ),
            "Quotes to Scrape": cleaned_counts.get(
                "Quotes to Scrape", 0
            ),
            "total": len(cleaned_records),
        },

        "rejected_records": {
            "Books to Scrape": rejected_counts.get(
                "Books to Scrape", 0
            ),
            "Quotes to Scrape": rejected_counts.get(
                "Quotes to Scrape", 0
            ),
            "total": len(invalid_records),
        },

        "rejection_reasons": rejection_reasons,

        "duplicates_removed": duplicates_removed,

        "final_records": {
            "Books to Scrape": final_counts.get(
                "Books to Scrape", 0
            ),
            "Quotes to Scrape": final_counts.get(
                "Quotes to Scrape", 0
            ),
            "total": len(final_records),
        },

        "output_file": CSV_PATH,
        "log_file": LOG_PATH,
    }

    with open(
        JSON_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    logger.info(
        "Summary saved: %s",
        JSON_PATH
    )

    logger.info(
        "Pipeline completed in %.2f seconds",
        duration_seconds
    )

    print("\nPipeline completed successfully!")
    print(f"Books scraped: {len(books)}")
    print(f"Quotes scraped: {len(quotes)}")
    print(f"Total raw records: {len(raw_records)}")
    print(f"Rejected records: {len(invalid_records)}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final records: {len(final_records)}")
    print(f"CSV: {CSV_PATH}")
    print(f"Summary: {JSON_PATH}")
    print(f"Log: {LOG_PATH}")


if __name__ == "__main__":
    main()