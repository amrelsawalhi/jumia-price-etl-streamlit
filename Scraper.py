import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random

# Global tracker for throttling repeat queries
recent_queries = {}
ua = UserAgent()

def scrape_jumia(product_name, max_results=10):
    product_name = product_name.strip().lower()
    query = product_name.replace(" ", "+")
    base_url = "https://www.jumia.com.eg/catalog/?q="
    url = base_url + query

    # Throttle repeat queries
    now = time.time()
    if product_name in recent_queries and now - recent_queries[product_name] < 30:
        print(f"[Throttle] Recent query for '{product_name}' — pausing 10s")
        time.sleep(10)
    recent_queries[product_name] = now

    # Simulate human-like behavior
    time.sleep(random.uniform(2.5, 5.0))

    # Rotate user-agent
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=20)
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print("Request failed:", e)
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("article.prd")
    print(f"Found {len(products)} raw product blocks for '{product_name}'")

    results = []
    for product in products:
        try:
            title_elem = product.select_one("h3.name")
            title = title_elem.text.strip() if title_elem else None

            price_elem = product.select_one("div.prc")
            price_text = price_elem.text.strip().replace("EGP", "").replace(",", "") if price_elem else None

            # Handle price ranges
            if price_text and "-" in price_text:
                price = float(price_text.split("-")[0].strip())  # Take the min value
            elif price_text:
                price = float(price_text)
            else:
                price = None

            link_elem = product.select_one("a.core")
            link = "https://www.jumia.com.eg" + link_elem["href"] if link_elem else None

            rating_elem = product.select_one("div.stars")
            rating = rating_elem["aria-label"] if rating_elem and "aria-label" in rating_elem.attrs else None

            if title and price and link:
                results.append({
                    "title": title,
                    "price_egp": price,
                    "rating": rating,
                    "link": link
                })

            if len(results) >= max_results:
                break

        except Exception as e:
            print("Skipping item due to error:", e)
            continue

    return pd.DataFrame(results)
