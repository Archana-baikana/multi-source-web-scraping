
# AI Usage Documentation

## AI Tools Used

ChatGPT was used as an AI-assisted development and learning tool during this assignment.

## Purpose of AI Assistance

AI assistance was used to:

- Understand the assessment requirements
- Plan the project structure
- Understand the scraping workflow
- Generate initial implementation ideas
- Understand Requests and BeautifulSoup usage
- Implement pagination logic
- Design the common data schema
- Implement cleaning, validation, and deduplication logic
- Create automated pytest tests
- Troubleshoot Python import and testing issues
- Review the overall pipeline structure
- Improve project documentation

## Prompts / Assistance Examples

Examples of prompts used during development included:

- Explain how to build a Python web scraping pipeline with multiple sources.
- Help implement pagination using Requests and BeautifulSoup.
- Explain how to normalize data from different sources into a common schema.
- Help implement data cleaning, validation, and deduplication.
- Help create pytest tests for the processing modules.
- Help troubleshoot Python package import errors during pytest execution.
- Review the project structure and identify missing requirements.
- Review the implementation against the assignment reference requirements.

## Parts Assisted by AI

AI assistance contributed to the initial implementation and development of:

- Scraper structure
- Pagination approach
- Shared HTTP client
- Cleaning functions
- Validation functions
- Deduplication logic
- Main pipeline orchestration
- Test cases
- README documentation
- AI usage documentation

## Human Verification and Corrections

The generated code was not used blindly.

The implementation was manually executed and verified against the target websites and assignment requirements.

Verification included:

- Running the Books scraper successfully
- Confirming 1000 books were scraped
- Running the Quotes scraper successfully
- Confirming 100 quotes were scraped
- Running the complete ETL pipeline
- Confirming 1100 raw records were processed
- Confirming 1100 records passed validation
- Confirming 1 duplicate was removed
- Confirming 1099 final records were generated
- Verifying the generated CSV file
- Verifying the generated JSON summary report
- Verifying numeric prices and ratings
- Verifying book detail page URLs
- Verifying quote authors and tags
- Verifying page-level logging
- Running the automated test suite successfully

## Testing Result

The final test suite contains 9 tests.

The tests cover:

- Text cleaning
- Price cleaning
- Rating cleaning
- Tag cleaning
- Quote quotation-mark removal
- Valid record validation
- Invalid record validation
- Book duplicate detection
- Quote duplicate detection

## Human Responsibility

The final implementation, execution, testing, verification, and submission preparation were reviewed manually.

AI was used as an assistant for development and explanation, while the resulting implementation was tested against the actual assignment requirements.

The final pipeline successfully produced:

```text
Books scraped:       1000
Quotes scraped:       100
Total raw records:   1100
Rejected records:       0
Duplicates removed:     1
Final records:       1099
```

The generated output files are:

```text
output/final_dataset.csv
output/summary_report.json
logs/scraper.log
```