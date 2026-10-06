

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"


def scrape_books():
    books = []
    page_url = BASE_URL

    while page_url:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select("article.product_pod"):
            title = book.h3.a.get("title")
            price = book.select_one(".price_color").get_text(strip=True)
            rating = book.select_one(".star-rating").get("class")[1]

            books.append({
                "name_or_title": title,
                "price": price,
                "rating": rating,
                "source": "Books to Scrape",
                "source_url": page_url,
            })

        next_button = soup.select_one("li.next a")

        if next_button:
            next_page = next_button.get("href")
            page_url = requests.compat.urljoin(page_url, next_page)
        else:
            page_url = None

    return books


if __name__ == "__main__":
    data = scrape_books()

    print(f"Total books scraped: {len(data)}")
    print(data[:3])