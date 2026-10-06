import logging

import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("scraper")

class HTTPClient:
    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; RealisierenScraper/1.0)"
        })

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    def get(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(0.5)
            return response

        except requests.RequestException as error:
            logger.error(
                "Request failed for %s: %s",
                url,
                error
            )
            raise

     