import json
import logging
import os
from datetime import datetime, timezone

import pandas as pd

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes
from processing.cleaning import clean_record
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


# Create output and logs folders if they don't exist
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# Configure logging
logging.basicConfig(
    filename="logs/scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("Scraping pipeline started")

    # 1. Scrape Books
    try:
        books = scrape_books()
        logging.info(f"Books scraped: {len(books)}")
    except Exception as error:
        logging.error(f"Books scraping failed: {error}")
        books = []

    # 2. Scrape Quotes
    try:
        quotes = scrape_quotes()
        logging.info(f"Quotes scraped: {len(quotes)}")
    except Exception as error:
        logging.error(f"Quotes scraping failed: {error}")
        quotes = []

    # 3. Combine raw data
    records = books + quotes

    logging.info(f"Total raw records: {len(records)}")

    # 4. Add common fields
    for record in records:
        record.setdefault("category", "")
        record.setdefault("price", "")
        record.setdefault("author", "")
        record.setdefault("tags", [])
        record.setdefault("description", "")
        record.setdefault(
            "scraped_at",
            datetime.now(timezone.utc).isoformat()
        )

    # 5. Clean records
    cleaned_records = [
        clean_record(record)
        for record in records
    ]

    # 6. Validate records
    valid_records, invalid_records = validate_records(
        cleaned_records
    )

    logging.info(f"Valid records: {len(valid_records)}")
    logging.info(f"Invalid records: {len(invalid_records)}")

    # 7. Deduplicate
    unique_records = deduplicate_records(valid_records)

    duplicates_removed = (
        len(valid_records) - len(unique_records)
    )

    logging.info(
        f"Duplicates removed: {duplicates_removed}"
    )

    # 8. Convert to DataFrame
    dataframe = pd.DataFrame(unique_records)

    # Make sure columns are in the required order
    columns = [
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

    for column in columns:
        if column not in dataframe.columns:
            dataframe[column] = ""

    dataframe = dataframe[columns]

    # 9. Save CSV
    csv_path = "output/final_dataset.csv"
    dataframe.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    # 10. Create summary report
    summary = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "books_scraped": len(books),
        "quotes_scraped": len(quotes),
        "total_raw_records": len(records),
        "valid_records": len(valid_records),
        "invalid_records": len(invalid_records),
        "duplicates_removed": duplicates_removed,
        "final_records": len(unique_records),
        "output_file": csv_path,
    }

    json_path = "output/summary_report.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    logging.info("Scraping pipeline completed")

    print("Pipeline completed successfully!")
    print(f"Books scraped: {len(books)}")
    print(f"Quotes scraped: {len(quotes)}")
    print(f"Total records: {len(records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records: {len(invalid_records)}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final records: {len(unique_records)}")
    print(f"CSV: {csv_path}")
    print(f"Summary: {json_path}")


if __name__ == "__main__":
    main()