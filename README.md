# Jumia Egypt Price Tracker

A web scraper that extracts product information from Jumia Egypt and displays it in a Streamlit interface.


## Features

- Search multiple products at once
- Displays product name, price (EGP), rating, and link
- Configurable maximum results per search
- Export results to CSV
- Randomized user agents to avoid detection
- Built with Python using Streamlit, BeautifulSoup, and requests

## Installation

1. Clone this repository:
    ```bash
   git clone https://github.com/amrelsawalhi/jumia-price-etl-streamlit.git
   cd jumia-price-etl-streamlit
2. Install the required packages: 
    ```bash
    pip install -r requirements.txt


## Usage

1. Run the application:  
    ```bash
    streamlit run jumia_scraper.py
2. Enter one or more product names (one per line)
3. Adjust the "Max products per search" slider
4. Click "Scrape Now" to start scraping
5. View results in the table and download as CSV if desired

## Notes

- This tool is for educational purposes only
- Jumia may block your IP if you make too many requests
- Web scraping may violate Jumia's terms of service
- Prices and availability may not be accurate

## License

MIT