import streamlit as st
import pandas as pd
from Scraper import scrape_jumia  # your existing scraping function

st.title("Jumia Egypt Product Scraper")

st.write("Enter product names, one per line:")
input_text = st.text_area("Product List", value="headphones\npower bank\nsmart watch")

max_results = st.slider("Max results per product", 3, 20, 5)

if st.button("Scrape All"):
    product_list = [line.strip() for line in input_text.splitlines() if line.strip()]
    all_data = []

    with st.spinner(f"Scraping {len(product_list)} product queries..."):
        for product in product_list:
            st.write(f"🔍 Scraping: `{product}`")
            df = scrape_jumia(product, max_results=max_results)
            if not df.empty:
                df["searched_product"] = product
                all_data.append(df)
            else:
                st.warning(f"No results for: {product}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        st.success(f"✅ Scraped {len(final_df)} total results.")
        st.dataframe(final_df)
        csv = final_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, file_name="jumia_prices.csv", mime="text/csv")
    else:
        st.warning("❌ No data scraped. Try different keywords.")

df = scrape_jumia("headphones", max_results=5)
st.write(df)
