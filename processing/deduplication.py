
def deduplicate_records(records):
    unique_records = []
    seen = set()

    for record in records:
        key = (
            record.get("source", ""),
            record.get("name_or_title", "").strip().lower(),
            record.get("author", "").strip().lower(),
        )

        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    return unique_records