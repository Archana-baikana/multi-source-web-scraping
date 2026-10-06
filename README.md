

# Multi-Source Web Scraping & Data Consolidation

## Overview

This project implements a Python-based web scraping and data consolidation pipeline that collects data from multiple web sources, cleans and validates the scraped records, removes duplicates, and generates a consolidated dataset.

### Data Sources

1. **Books to Scrape** — https://books.toscrape.com/
2. **Quotes to Scrape** — https://quotes.toscrape.com/

## Features

- Scrapes data from multiple web sources
- Handles pagination
- Extracts source-specific fields
- Normalizes records into a common schema
- Cleans scraped data
- Validates required fields
- Removes duplicate records
- Handles scraping failures using exception handling
- Generates logging information
- Exports the final dataset to CSV
- Generates a JSON summary report
- Includes automated tests using pytest

## Technology Stack

- Python
- Requests
- BeautifulSoup
- Pandas
- Pytest
- Python Logging

## Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraping.log
│
├── tests/
│   ├── __init__.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd scraping_assignment
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Pipeline

Run the complete scraping and processing pipeline with:

```bash
python main.py
```

The pipeline performs:

```text
Books Scraper ──┐
                ├──> Combine Data
Quotes Scraper ─┘
                     ↓
                  Cleaning
                     ↓
                 Validation
                     ↓
                Deduplication
                     ↓
                Final Dataset
```

## Output

The pipeline generates:

### CSV

```text
output/final_dataset.csv
```

The standardized schema contains:

- `source`
- `source_url`
- `name_or_title`
- `category`
- `price`
- `rating`
- `author`
- `tags`
- `description`
- `scraped_at`

### JSON Summary

```text
output/summary_report.json
```

The summary contains:

- Number of books scraped
- Number of quotes scraped
- Total raw records
- Valid records
- Invalid records
- Duplicates removed
- Final record count
- Output file location

## Logging

Pipeline activity and scraping failures are recorded in:

```text
logs/scraping.log
```

The logging system records important pipeline events such as the number of records scraped, validation results, duplicate removal, and completion status.

## Testing

Automated tests are written using pytest.

Run:

```bash
pytest -q
```

The current test suite verifies:

- Text cleaning
- Price cleaning
- Tag cleaning
- Record validation
- Duplicate removal

## Error Handling

Each scraper is executed inside exception handling in the main pipeline.

If one source fails, the pipeline logs the error and continues processing the available data from the other source.

## Assumptions

- The target websites are publicly accessible.
- The websites use predictable HTML structures.
- Missing source-specific fields are represented as empty values in the common schema.
- Records from different sources are not considered duplicates solely because their titles/text are similar.
- Duplicate detection uses source, title/text, and author as the identifying fields.

## Current Run

The pipeline successfully processed:

```text
Books scraped:       1000
Quotes scraped:       100
Total raw records:   1100
Valid records:       1100
Invalid records:        0
Duplicates removed:     1
Final records:       1099
```

## Future Improvements

Possible production improvements include:

- Retry logic with exponential backoff
- More detailed source-specific validation
- Configurable scraping URLs
- Parallel/asynchronous scraping
- Database storage
- Docker support
- More extensive test coverage
- Monitoring and alerting