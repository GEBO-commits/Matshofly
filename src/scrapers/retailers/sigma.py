
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

    def extract_specifications(self, soup: BeautifulSoup) -> dict:
        
        containers = [
            soup.select_one('[id$="content-specifications"]'),
            soup.select_one("#specifications-list")
        ]
        for container in containers:
            specifications = {}
            if container is None:
                continue
            # Process the container for specifications
            rows = container.select(":scope > div")
            for row in rows:
                paragraphs = row.select(":scope > p")
                if len(paragraphs)<2:
                    continue
                label = paragraphs[0].get_text(strip=True).rstrip(":")
                value = paragraphs[1].get_text(strip=True)
                specifications[label] = value

            if specifications:
                return specifications
        return {}