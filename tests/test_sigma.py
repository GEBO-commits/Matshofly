from bs4 import BeautifulSoup
from src.scrapers.retailers.sigma import SigmaScraper

html = """
<div id="specifications-list">
    <div><p>Model:</p><p>RTX 4070 SUPER</p></div>
    <div><p>Memory:</p><p>12GB GDDR6X</p></div>
</div>
"""

soup = BeautifulSoup(html, "html.parser")
scraper = SigmaScraper()

result = scraper.extract_specifications(soup)

print(result)