

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://quotes.toscrape.com/"


def scrape_quotes():
    quotes = []
    page_url = BASE_URL

    while page_url:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.select("div.quote"):
            text = quote.select_one("span.text").get_text(strip=True)
            author = quote.select_one("small.author").get_text(strip=True)

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

        next_button = soup.select_one("li.next a")

        if next_button:
            next_page = next_button.get("href")
            page_url = requests.compat.urljoin(page_url, next_page)
        else:
            page_url = None

    return quotes


if __name__ == "__main__":
    data = scrape_quotes()

    print(f"Total quotes scraped: {len(data)}")
    print(data[:3])