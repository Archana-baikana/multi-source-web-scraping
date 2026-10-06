
def validate_record(record):
    """Validate one cleaned record and return validation errors."""
    errors = []

    required_fields = [
        "source",
        "source_url",
        "name_or_title",
    ]

    for field in required_fields:
        if not record.get(field):
            errors.append(f"{field} is required")

    price = record.get("price")

    if price not in ("", None):
        if not isinstance(price, (int, float)):
            errors.append("price must be numeric")
        elif price < 0:
            errors.append("price cannot be negative")

    rating = record.get("rating")

    if rating not in ("", None):
        if not isinstance(rating, int):
            errors.append("rating must be an integer")
        elif not 1 <= rating <= 5:
            errors.append("rating must be between 1 and 5")

    return errors


def validate_records(records):
    """Separate valid and invalid records."""
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