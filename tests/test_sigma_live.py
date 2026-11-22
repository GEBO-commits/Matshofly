import requests
from bs4 import BeautifulSoup
from src.scrapers.retailers.sigma import SigmaScraper

url = "https://www.sigma-computer.com/en/item?id=msi-pro-b760m-a-ddr4-ii-lga-1700-motherboard-jhaelhiijpcu"

response = requests.get(url, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
layout_a = soup.select_one('[id$="content-specifications"]')
layout_b = soup.select_one("#specifications-list")

print("Layout A rows:", len(layout_a.select(":scope > div")) if layout_a else 0)
print("Layout B rows:", len(layout_b.select(":scope > div")) if layout_b else 0)

scraper = SigmaScraper()
specifications = scraper.extract_specifications(soup)
chipset = soup.find(string="Chipset")


# for row in layout_a.select(":scope > div"):
#     paragraphs = row.select(":scope > p")

#     if len(paragraphs) >= 2:
#         if paragraphs[0].get_text(strip=True) == "Chipset":
#             print(paragraphs[1].prettify())    

# print("Specifications found:", len(specifications))
# print(specifications)
# print("Status:", response.status_code)
# print("Layout A:", "content-specifications" in response.text)
# print("Layout B:", "specifications-list" in response.text)
print("Extracted:", repr(specifications.get("Chipset")))

layout_a = soup.select_one('[id$="content-specifications"]')

for row in layout_a.select(":scope > div"):
    paragraphs = row.select(":scope > p")

    if len(paragraphs) >= 2 and paragraphs[0].get_text(strip=True) == "Chipset":
        print("Direct extraction:", repr(paragraphs[1].get_text(strip=True)))
