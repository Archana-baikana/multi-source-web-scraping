
import requests

from bs4 import BeautifulSoup

from scrapers.http_client import HTTPClient


BASE_URL = "https://quotes.toscrape.com/"


def scrape_quotes():
    quotes = []
    page_url = BASE_URL
    client = HTTPClient()

    while page_url:
        response = client.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.select("div.quote"):
            try:
                text_element = quote.select_one("span.text")
                author_element = quote.select_one("small.author")

                if not text_element or not author_element:
                    continue

                text = text_element.get_text(" ", strip=True)
                author = author_element.get_text(strip=True)

                tags = [
                    tag.get_text(strip=True)
                    for tag in quote.select("div.tags a.tag")
                ]

                quotes.append({
                    "name_or_title": text,
                    "author": author,
                    "tags": tags,
                    "source": "Quotes to Scrape",
                    "source_url": page_url,
                })

            except Exception as error:
                print(f"Skipping invalid quote record: {error}")

        next_button = soup.select_one("li.next a")

        if next_button:
            next_page = next_button.get("href")
            page_url = requests.compat.urljoin(
                page_url,
                next_page
            )
        else:
            page_url = None

    return quotes


if __name__ == "__main__":
    data = scrape_quotes()

    print(f"Total quotes scraped: {len(data)}")
    print(data[:3])