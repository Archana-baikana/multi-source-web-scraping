
def clean_text(value):
    if value is None:
        return ""

    return " ".join(str(value).split())


def clean_price(price):
    if not price:
        return ""

    price = str(price).replace("Â£", "£")
    return price.strip()


def clean_tags(tags):
    if not tags:
        return []

    if isinstance(tags, list):
        return [clean_text(tag) for tag in tags]

    return [clean_text(tags)]


def clean_record(record):
    cleaned = record.copy()

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title", "")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category", "")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price", "")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author", "")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description", "")
    )

    cleaned["tags"] = clean_tags(
        cleaned.get("tags", [])
    )

    return cleaned