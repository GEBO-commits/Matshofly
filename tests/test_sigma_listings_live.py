
import requests
from bs4 import BeautifulSoup
from src.scrapers.retailers.sigma import SigmaScraper


# Initialize Sigma scraper
scraper = SigmaScraper()

# Sigma laptop category
url = (
    "https://www.sigma-computer.com/en/search"
    "?filters=%7B%22category_id%22%3A%5B"
    "%229f5039de-5c80-46f3-9fe4-6e8f94189b8c%22"
    "%5D%7D"
)

# Fetch the category page
response = requests.get(url, timeout=15)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")


# --------------------------------
# 1. HTTP response verification
# --------------------------------

print("\n=== HTTP RESPONSE ===")
print("Status:", response.status_code)
print("Final URL:", response.url)


# --------------------------------
# 2. Product link discovery
# --------------------------------

print("\n=== LINK DISCOVERY ===")

product_links = soup.select('a[href*="/en/item?id="]')

title_links = soup.select(
    'a.line-clamp-2[href*="/en/item?id="]'
)

unique_urls = {
    link.get("href")
    for link in title_links
}

print("All product links:", len(product_links))
print("Title links:", len(title_links))
print("Unique product URLs:", len(unique_urls))


# --------------------------------
# 3. Extract product listings
# --------------------------------

print("\n=== PRODUCT EXTRACTION ===")

products = scraper.extract_product_listings(soup)

print("Products found:", len(products))

for product in products[:5]:
    print(product)


# --------------------------------
# 4. Missing price validation
# --------------------------------

print("\n=== PRICE VALIDATION ===")

missing_prices = [
    product
    for product in products
    if product["price"] is None
]

print("Products with missing prices:", len(missing_prices))


# --------------------------------
# 5. Investigate suspicious price
# --------------------------------

print("\n=== LEGION PRO 7 INVESTIGATION ===")

found = False

for link in title_links:

    if "legion pro 7" in link.get_text(strip=True).lower():

        found = True

        card = link.parent.parent

        price_element = card.select_one(
            "p.text-sigma-blue-600"
        )

        print("Product:", link.get_text(strip=True))

        if price_element:
            print("Raw price HTML:")
            print(price_element.prettify())

            print(
                "Raw price text:",
                repr(price_element.get_text(strip=True))
            )
        else:
            print("Price element not found.")

if not found:
    print("Legion Pro 7 not found on this page.")
