
REQUIRED_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "author",
    "tags",
    "description",
    "scraped_at",
]


def validate_record(record):
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Missing field: {field}")

    # Title should not be empty
    if not record.get("name_or_title"):
        errors.append("name_or_title is empty")

    # Source should not be empty
    if not record.get("source"):
        errors.append("source is empty")

    # Source URL should not be empty
    if not record.get("source_url"):
        errors.append("source_url is empty")

    return errors


def validate_records(records):
    valid_records = []
    invalid_records = []

    for record in records:
        errors = validate_record(record)

        if errors:
            invalid_records.append({
                "record": record,
                "errors": errors,
            })
        else:
            valid_records.append(record)

    return valid_records, invalid_records