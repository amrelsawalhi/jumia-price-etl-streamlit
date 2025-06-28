import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import time
import random

def scrape_jumia(product_name, max_results=10):
    product_name = product_name.strip().lower()
    query = product_name.replace(" ", "+")
    url = f"https://www.jumia.com.eg/catalog/?q={query}"

    headers = {
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9"
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=20)
        if response.status_code != 200:
            return []
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("article.prd")

    results = []
    for product in products:
        try:
            title_elem = product.select_one("h3.name")
            title = title_elem.text.strip() if title_elem else None

            price_elem = product.select_one("div.prc")
            price_text = price_elem.text.strip().replace("EGP", "").replace(",", "") if price_elem else None
            if price_text and "-" in price_text:
                price = float(price_text.split("-")[0].strip())
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
                    "Product": title,
                    "Price (EGP)": price,
                    "Rating": rating,
                    "Link": link
                })

            if len(results) >= max_results:
                break
        except Exception:
            continue

    return results

# Streamlit UI
st.set_page_config(page_title="Jumia Price Tracker", layout="wide")

st.title("🛒 Jumia Egypt Price Tracker")
st.write("Enter one or more product names (one per line):")

user_input = st.text_area("Products to search", height=200, placeholder="e.g. iPhone 13\nAir fryer\nGaming chair")

max_results = st.slider("Max products per search", 3, 20, 10)

if st.button("Scrape Now"):
    if not user_input.strip():
        st.warning("Please enter at least one product.")
    else:
        queries = [q.strip() for q in user_input.strip().splitlines() if q.strip()]
        all_results = []
        with st.spinner("Scraping Jumia..."):
            for q in queries:
                st.write(f"🔍 Searching: **{q}**")
                time.sleep(random.uniform(2.5, 5.0))
                results = scrape_jumia(q, max_results=max_results)
                for item in results:
                    item["Search Term"] = q
                all_results.extend(results)

        if all_results:
            df = pd.DataFrame(all_results)
            df = df[["Search Term", "Product", "Price (EGP)", "Rating", "Link"]]
            st.success(f"✅ {len(df)} items scraped.")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name="jumia_results.csv", mime="text/csv")
        else:
            st.warning("No results found.")
