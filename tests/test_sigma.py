from bs4 import BeautifulSoup
from src.scrapers.retailers.sigma import SigmaScraper
def test_product_listings():
    
    
    pass



html = html = """
<div class="product-card">
    <div>
        <a class="chakra-tooltip__trigger"
           href="/en/item?id=msi-motherboard">
            MSI Motherboard
        </a>
        <p class="text-sigma-blue-600">7650 EGP</p>
    </div>
</div>

<div class="product-card">
    <div>
        <a class="chakra-tooltip__trigger"
           href="/en/item?id=asus-gpu">
            ASUS RTX 4070 SUPER
        </a>
    </div>
</div>
"""
soup = BeautifulSoup(html, "html.parser")
scraper = SigmaScraper()

result = scraper.extract_specifications(soup)
result_products = scraper.extract_product_listings(soup)
assert len(result_products) == 2
assert result_products[0]["name"] == "MSI Motherboard"
assert result_products[0]["url"] == "https://www.sigma-computer.com/en/item?id=msi-motherboard"
assert result_products[0]["price"] == 7650
assert result_products[1]["name"] == "ASUS RTX 4070 SUPER"
assert result_products[1]["url"] == "https://www.sigma-computer.com/en/item?id=asus-gpu"
assert result_products[1]["price"] is None


if __name__ == "__main__":
    test_product_listings()
    print("Product listing test passed!")