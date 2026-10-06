
import re


RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def clean_text(value):
    """Normalize whitespace and remove unnecessary spaces."""
    if value is None:
        return ""

    text = str(value).replace("\xa0", " ")
    return " ".join(text.split())


def strip_quotes(value):
    """Remove curly quote characters around quote text."""
    if value is None:
        return ""

    text = clean_text(value)

    quote_marks = {"“", "”", '"', "‘", "’"}

    while text and text[0] in quote_marks:
        text = text[1:].strip()

    while text and text[-1] in quote_marks:
        text = text[:-1].strip()

    return text


def clean_price(price):
    """Convert a price such as £51.77 into numeric 51.77."""
    if price is None or price == "":
        return None

    price_text = str(price).replace("Â£", "£").strip()
    price_text = re.sub(r"[^\d.]", "", price_text)

    if not price_text:
        return None

    try:
        return float(price_text)
    except ValueError:
        return None


def clean_rating(rating):
    """Convert rating words such as Three into integer 3."""
    if rating is None or rating == "":
        return None

    rating_text = clean_text(rating)

    if rating_text in RATING_MAP:
        return RATING_MAP[rating_text]

    try:
        rating_number = int(rating_text)

        if 1 <= rating_number <= 5:
            return rating_number

    except ValueError:
        pass

    return None


def clean_tags(tags):
    """Clean quote tags and return them as a list."""
    if not tags:
        return []

    if isinstance(tags, list):
        return [clean_text(tag) for tag in tags if clean_text(tag)]

    return [clean_text(tags)]


def clean_record(record):
    """Clean one scraped record."""
    cleaned = record.copy()

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title", "")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category", "")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
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

    # Quotes contain curly quotation marks.
    if cleaned.get("source") == "Quotes to Scrape":
        cleaned["name_or_title"] = strip_quotes(
            cleaned.get("name_or_title", "")
        )

    return cleaned