
# Multi-Source Web Scraping & Data Consolidation

## Overview

This project implements a Python-based ETL pipeline that collects data from two practice websites:

- Books to Scrape
- Quotes to Scrape

The pipeline follows these stages:

```text
Scrape
   ↓
Clean
   ↓
Validate
   ↓
Deduplicate
   ↓
Consolidate
   ↓
Save
```

The final output is a consolidated CSV dataset and a JSON summary report.

## Data Sources

### 1. Books to Scrape

URL:

```text
https://books.toscrape.com/
```

Expected records:

- Approximately 1000 books
- 50 pages

### 2. Quotes to Scrape

URL:

```text
https://quotes.toscrape.com/
```

Expected records:

- 100 quotes
- 10 pages

Only these two practice websites are scraped.

---

## Technology Stack

- Python 3.10–3.12 required by the assignment specification
- requests
- BeautifulSoup4
- lxml
- pytest
- Python standard library:
  - csv
  - json
  - logging
  - re
  - urllib.parse
  - time
  - pathlib
  - datetime

> Note: The project was developed and executed successfully in the submitted local environment using Python 3.9.12. The assignment reference specifies Python 3.10–3.12.

---

## Stage 1: HTML Structure Observations

### Books to Scrape

Each book is represented by:

```text
article.product_pod
```

Fields:

- Title: `h3 > a`
- Full title: `title` attribute of the link
- Price: `p.price_color`
- Rating: class on `p.star-rating`
- Book link: `h3 > a[href]`
- Next page: `li.next > a`

The Books listing page does not expose author information.

Category and description are not available in the listing data used by this implementation, so these fields are left empty rather than guessed.

The `source_url` for books is the individual book detail page URL.

### Quotes to Scrape

Each quote is represented by:

```text
div.quote
```

Fields:

- Quote text: `span.text`
- Author: `small.author`
- Tags: `a.tag`
- Author link: `a[href^="/author/"]`
- Next page: `li.next > a`

The quote text is cleaned to remove surrounding curly quotation marks.

The `source_url` for quotes is the quote listing page URL.

---

## Pagination

Pagination is discovered dynamically from the HTML.

The scrapers do not hard-code page numbers.

For Books:

```text
li.next > a
```

For Quotes:

```text
li.next > a
```

Relative next-page links are converted into absolute URLs before requesting the next page.

The scraper continues until no `next` link is available.

---

## HTTP Handling

A shared HTTP client is used by both scrapers.

The HTTP client:

- Uses `requests.Session`
- Sends a custom User-Agent
- Uses a request timeout
- Retries temporary HTTP failures
- Retries status codes:
  - 429
  - 500
  - 502
  - 503
  - 504
- Pauses approximately 0.5 seconds between successful requests

No passwords, API keys, or authentication credentials are required.

---

## Common Data Model

All records are normalized into the following common schema:

| Field | Description |
|---|---|
| `source` | Source website name |
| `source_url` | URL associated with the scraped record |
| `name_or_title` | Book title or quote text |
| `category` | Category when available |
| `price` | Numeric price when available |
| `rating` | Integer rating from 1 to 5 when available |
| `author` | Author when available |
| `tags` | Semicolon-separated tags |
| `description` | Description when available |
| `scraped_at` | UTC timestamp |

### Books Mapping

```text
source        = Books to Scrape
source_url    = Book detail page URL
name_or_title = Book title
category      = Empty when unavailable
price         = Numeric price
rating        = Integer 1-5
author        = Empty
tags          = Empty
description   = Empty when unavailable
scraped_at    = UTC timestamp
```

### Quotes Mapping

```text
source        = Quotes to Scrape
source_url    = Quote listing page URL
name_or_title = Quote text
category      = Empty
price         = Empty
rating        = Empty
author        = Author name
tags          = Semicolon-separated tags
description   = Empty
scraped_at    = UTC timestamp
```

---

## Cleaning

Cleaning is performed before validation.

### Text Cleaning

Extra spaces, tabs, newlines, and non-breaking spaces are normalized.

Example:

```text
"  Example   Book  "
```

becomes:

```text
"Example Book"
```

### Quote Cleaning

Surrounding quotation marks are removed from quote text.

### Price Cleaning

Currency symbols and unwanted characters are removed.

Example:

```text
£51.77
```

becomes:

```text
51.77
```

### Rating Cleaning

Text ratings are converted to integers.

Examples:

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

### Tags

Quote tags are cleaned and stored as a semicolon-separated string in the final CSV.

Example:

```text
change;deep-thoughts;thinking;world
```

---

## Validation

Each cleaned record is validated before being added to the final dataset.

Required fields:

- `source`
- `source_url`
- `name_or_title`

Additional validation:

- Price must be numeric when present.
- Price cannot be negative.
- Rating must be an integer when present.
- Rating must be between 1 and 5.

Invalid records are rejected without crashing the complete pipeline.

Each rejected record is logged with its validation reason.

---

## Deduplication

Duplicate records are removed after validation.

Text normalization is applied before generating fingerprints so differences in spacing and capitalization do not prevent duplicate detection.

### Books

Book fingerprint:

```text
source + normalized title
```

Therefore:

```text
Example Book
 example book
EXAMPLE BOOK
```

are treated as the same book.

### Quotes

Quote fingerprint:

```text
source + normalized author + first 50 characters of normalized quote text
```

Duplicates are dropped from the final dataset.

The number of removed duplicates is included in `summary_report.json`.

---

## Error Handling

The pipeline uses exception handling at both record and source levels.

### Record-level failures

If an individual record cannot be parsed correctly, that record is skipped instead of stopping the complete scraper.

### Source-level failures

If one source fails, the error is logged and the pipeline continues with the other source.

### Failed requests

Temporary HTTP failures are retried by the shared HTTP client.

---

## Logging

Logging is written to:

```text
logs/scraper.log
```

The pipeline logs:

- Pipeline start
- Source scraping start/completion
- Record counts
- Validation results
- Rejected records
- Duplicate removal
- Output creation
- Pipeline completion
- Errors

Console logging is also enabled.

---

## Output Files

### Final CSV

```text
output/final_dataset.csv
```

The CSV uses a fixed column order:

```text
source
source_url
name_or_title
category
price
rating
author
tags
description
scraped_at
```

### Summary JSON

```text
output/summary_report.json
```

The summary contains:

- Start time
- End time
- Duration
- Raw records per source
- Records after cleaning
- Rejected records
- Rejection reasons
- Duplicates removed
- Final records per source
- Total final records
- Output file location
- Log file location

The counts reconcile using:

```text
raw records - rejected records - duplicates removed = final records
```

---

## Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── books_scraper.py
│   ├── quotes_scraper.py
│   └── http_client.py
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
│   └── scraper.log
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

---

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

---

## Running the Pipeline

Run:

```bash
python main.py
```

The pipeline will:

1. Scrape Books to Scrape.
2. Scrape Quotes to Scrape.
3. Clean the records.
4. Validate the records.
5. Remove duplicates.
6. Consolidate the datasets.
7. Save the final CSV.
8. Generate the JSON summary.
9. Write logs.

---

## Testing

Run:

```bash
pytest -q
```

The test suite covers:

- Text cleaning
- Price cleaning
- Rating cleaning
- Tag cleaning
- Quote quote-mark removal
- Record validation
- Invalid price/rating handling
- Book duplicate detection
- Quote duplicate detection

---

## Current Run

The latest successful pipeline execution produced:

```text
Books scraped:       1000
Quotes scraped:       100
Total raw records:   1100
Valid records:       1100
Invalid records:        0
Duplicates removed:     1
Final records:       1099
```

The reconciliation is:

```text
1100 - 0 - 1 = 1099
```

---

## Assumptions and Limitations

- Only Books to Scrape and Quotes to Scrape are scraped.
- The websites are assumed to be publicly accessible.
- Missing source-specific fields are represented by empty values.
- Book category and description are left empty because they are not available in the listing data used by this implementation.
- Book author information is not available on the listing page and is therefore left empty.
- Quote `source_url` is the listing page URL.
- Duplicate records are dropped rather than flagged.
- The scraper depends on the current HTML structure of the practice websites.

---

## AI Usage

AI assistance was used during development for:

- Understanding assignment requirements
- Structuring the ETL pipeline
- Debugging Python code
- Designing cleaning and validation logic
- Creating unit-test cases
- Improving documentation

The final implementation was tested locally, and the developer understands the main scraping, processing, validation, deduplication, and output-generation logic.

Detailed AI usage is documented separately in:

```text
AI_USAGE.md
```