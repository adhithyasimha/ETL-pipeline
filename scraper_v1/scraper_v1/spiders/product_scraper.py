from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import json
from urllib.parse import urlparse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Accept-language': 'en-US, en;q=0.5'
}

# Helper Functions 

def fetch_soup(url):
    """Fetch and parse a webpage."""
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser")


def get_location_from_jsonld(soup):
    """Try extracting seller location from JSON-LD."""
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string.strip())
        except Exception:
            continue

        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            addr = None
            if item.get("@type") == "Organization" and isinstance(item.get("address"), dict):
                addr = item["address"]
            elif item.get("@type") == "PostalAddress":
                addr = item

            if addr:
                city = (addr.get("addressLocality") or "").strip()
                state = (addr.get("addressRegion") or "").strip()
                country = (addr.get("addressCountry") or "").strip()
                pincode = (addr.get("postalCode") or "").strip()
                parts = [p for p in [city, state, pincode, country] if p]
                if parts:
                    return ", ".join(parts)
    return None


def extract_product_info(link, category, pre_location=None):
    """Extract product details from individual product page."""
    try:
        if not link.startswith("http"):
            link = "https://www.indiamart.com" + link

        product_webpage = requests.get(link, headers=HEADERS)
        product_soup = BeautifulSoup(product_webpage.text, "html.parser")

        # --- Product Name ---
        product_name = product_soup.find("h1", class_="bo center-heading centerHeadHeight")
        product_name = product_name.text.strip() if product_name else "N/A"

        # --- Price ---
        price_tag = product_soup.find("span", class_="bo price-unit")
        price = price_tag.text.strip() if price_tag else "N/A"
        unit_tag = product_soup.find("span", class_="bo unit")
        unit = unit_tag.text.strip() if unit_tag else ""

        if price != "N/A":
            if price.endswith("/"):
                price = f"{price}{unit if unit else 'Piece'}"
            elif unit and unit not in price:
                price = f"{price}/{unit}"


        supplier = product_soup.find("h2", class_="fs15")
        supplier = supplier.text.strip() if supplier else "N/A"


        location = get_location_from_jsonld(product_soup)
        if not location:
        
            candidates = [
                ("span", {"class": "sm clg"}),
                ("span", {"class": "bo seller-city"}),
                ("div", {"class": "addrs"}),
                ("div", {"id": "comp-loc"})
            ]
            for tag, attrs in candidates:
                el = product_soup.find(tag, attrs=attrs)
                if el and el.get_text(strip=True):
                    location = el.get_text(strip=True)
                    break
        if not location:
            location = pre_location or "N/A"

        
        rating = product_soup.find("span", class_="bo color")
        rating = rating.text.strip() if rating else "N/A"
        description = product_soup.find("div", id="descp2")
        description = description.text.strip().replace("\xa0", " ") if description else "N/A"

        return {
            "Product Name": product_name,
            "Category": category,
            "Price": price,
            "Supplier": supplier,
            "Location": location,
            "Rating": rating,
            "URL": link
        }

    except Exception as e:
        print(f"❌ Failed to scrape {link} due to {e}")
        return None


def scrape_category_page(url, category):
    """Scrape all product links and details from one category page."""
    products_data = []
    print(f"🔎 Scraping category: {url}")
    soup = fetch_soup(url)

    products_links = soup.find_all("a", class_="fs18 ptitle")
    for a_tag in products_links:
        link = a_tag.get("href")

        li = a_tag.find_parent("li")
        pre_city = li.get("data-city") if li else None
        pre_state = li.get("data-state") if li else None
        pre_loc = ", ".join([p for p in [pre_city, pre_state] if p])

        product_info = extract_product_info(link, category, pre_location=pre_loc)
        if product_info:
            products_data.append(product_info)
        time.sleep(2)  # polite delay

    return pd.DataFrame(products_data)


if __name__ == "__main__":
    all_dataframes = []

    with open("scraped_content/categories.json", "r", encoding="utf-8") as f:
        subcategories = json.load(f)

    for subcat in subcategories:
        url = subcat["subcategory_url"]
        category = subcat["category_key"]
        df = scrape_category_page(url, category)
        if not df.empty:
            all_dataframes.append(df)

    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)
        final_df.to_json("scraped_content/indiamart_products.json", orient="records", indent=2)
        print(f"✅ Saved {len(final_df)} products to 'indiamart_products.json'")
    else:
        print("⚠ No products found.")
