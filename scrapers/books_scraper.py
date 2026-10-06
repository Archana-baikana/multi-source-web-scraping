import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.http_client import HTTPClient


logger = logging.getLogger("scraper")

BASE_URL = "https://books.toscrape.com/"


def scrape_books():
    books = []
    page_url = BASE_URL
    client = HTTPClient()

    while page_url:
        logger.info("Books page: %s", page_url)

        response = client.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select("article.product_pod"):
            try:
                title_link = book.select_one("h3 > a")
                price_element = book.select_one("p.price_color")
                rating_element = book.select_one("p.star-rating")

                if not title_link or not price_element or not rating_element:
                    raise ValueError("Missing required book field")

                title = title_link.get("title")
                relative_url = title_link.get("href")

                if not title or not relative_url:
                    raise ValueError("Missing book title or URL")

                detail_url = urljoin(page_url, relative_url)

                price = price_element.get_text(strip=True)

                rating_classes = rating_element.get("class", [])
                rating = (
                    rating_classes[1]
                    if len(rating_classes) > 1
                    else ""
                )

                books.append({
                    "name_or_title": title,
                    "price": price,
                    "rating": rating,
                    "source": "Books to Scrape",
                    "source_url": detail_url,
                })

            except Exception as error:
                logger.warning(
                    "Skipping invalid book record on %s: %s",
                    page_url,
                    error
                )

        next_button = soup.select_one("li.next > a")

        if next_button:
            next_page = next_button.get("href")

            if next_page:
                page_url = urljoin(page_url, next_page)
            else:
                page_url = None
        else:
            page_url = None

    return books


if __name__ == "__main__":
    data = scrape_books()
    print(f"Total books scraped: {len(data)}")
    print(data[:3])