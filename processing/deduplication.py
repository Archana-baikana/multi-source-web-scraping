
def normalize_text(value):
    """Normalize text for duplicate comparison."""
    if value is None:
        return ""

    return " ".join(str(value).split()).strip().lower()


def deduplicate_records(records):
    """Remove duplicate records using source-specific fingerprints."""
    unique_records = []
    seen = set()

    for record in records:
        source = normalize_text(record.get("source"))
        title = normalize_text(record.get("name_or_title"))
        author = normalize_text(record.get("author"))

        if source == "books to scrape":
            fingerprint = (
                source,
                title,
            )

        elif source == "quotes to scrape":
            quote_prefix = title[:50]

            fingerprint = (
                source,
                author,
                quote_prefix,
            )

        else:
            fingerprint = (
                source,
                title,
            )

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_records.append(record)

    return unique_records