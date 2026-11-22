from turtle import delay

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time
import requests
from unittest.mock import Mock, patch, call

# Import fetch_page from whichever module you saved it in.

def test_fetch_page_retries_after_timeouts():
    mock_response = Mock(status_code=200)

    mock_get = Mock(
        side_effect=[
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            mock_response
        ]
    )

    # YOUR CODE HERE
    with patch("requests.get", mock_get), patch("time.sleep") as mock_sleep:
        response = fetch_page("https://example.com")
        assert response is mock_response
        assert mock_get.call_count == [call(2),call(4)]
        print(mock_sleep.call_args_list)
        assert mock_sleep.call_count == 2
class SigmaScraper:

    def __init__(self):
        self.base_url = "https://www.sigma-computer.com"

        self.category_selector = (
            "a.cursor-pointer[href*='/en/category/']"
        )

    def discover_categories(self, html):
        soup = BeautifulSoup(html, "html.parser")

        category_elements = soup.select(
            self.category_selector
        )

        categories = []

        for element in category_elements:
            name_element = element.select_one("span")

            if not name_element:
                continue

            category = {
                "name": name_element.get_text(strip=True),
                "url": urljoin(
                    self.base_url,
                    element.get("href", "")
                )
            }

            categories.append(category)

        return categories

    def extract_specifications(self, soup: BeautifulSoup) -> dict:
        containers = [
            soup.select_one('[id$="content-specifications"]'),
            soup.select_one("#specifications-list")
        ]

        for container in containers:
            if container is None:
                continue

            specifications = {}
            rows = container.select(":scope > div")

            for row in rows:
                paragraphs = row.select(":scope > p")

                if len(paragraphs) < 2:
                    continue

                label = paragraphs[0].get_text(strip=True).rstrip(":")
                value = paragraphs[1].get_text(strip=True)

                specifications[label] = value

            if specifications:
                return specifications

        return {}

    def extract_product_listings(self, soup: BeautifulSoup) -> list:
        title_links = soup.select(
            'a.line-clamp-2[href*="/en/item?id="]'
        )

        products = []

        for link in title_links:
            card = link.parent.parent

            product = {
                "name": link.get_text(strip=True),
                "url": urljoin(self.base_url, link.get("href", "")),
                "price": None
            }

            price_element = card.select_one(
                "p.text-sigma-blue-600"
            )

            if price_element:
                price_text = price_element.get_text(strip=True)
                clean_price = re.sub(r"\D", "", price_text)

                if clean_price:
                    product["price"] = int(clean_price)

            products.append(product)

        return products
def fetch_page(url: str):
    retryable_statuses = {500, 502, 503, 504}

    for attempt in range(4):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as error:
            print("Network error:", error)

        except requests.exceptions.HTTPError as error:
            status = error.response.status_code

            if status in retryable_statuses:
                print(f"Retryable HTTP error: {status}")
            else:
                print(f"Non-retryable HTTP error: {status}")
                return None

        if attempt < 3:
            delay_seconds = 2 ** (attempt + 1)
            time.sleep(delay_seconds)

    return None