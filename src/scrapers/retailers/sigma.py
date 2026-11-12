
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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
