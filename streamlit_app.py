import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Config ---
API_KEY = "e8f7788e76b24e45b9f7e57cbb6130f5"  # Replace with your key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# List of all available countries supported by NewsAPI
COUNTRIES = {
    'ae': 'United Arab Emirates',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'be': 'Belgium',
    'bg': 'Bulgaria',
    'br': 'Brazil',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cn': 'China',
    'co': 'Colombia',
    'cu': 'Cuba',
    'cz': 'Czech Republic',
    'de': 'Germany',
    'eg': 'Egypt',
    'fr': 'France',
    'gb': 'United Kingdom',
    'gr': 'Greece',
    'hk': 'Hong Kong',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'il': 'Israel',
    'in': 'India',
    'it': 'Italy',
    'jp': 'Japan',
    'kr': 'South Korea',
    'lt': 'Lithuania',
    'lv': 'Latvia',
    'ma': 'Morocco',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'ng': 'Nigeria',
    'nl': 'Netherlands',
    'no': 'Norway',
    'nz': 'New Zealand',
    'ph': 'Philippines',
    'pl': 'Poland',
    'pt': 'Portugal',
    'ro': 'Romania',
    'rs': 'Serbia',
    'ru': 'Russia',
    'sa': 'Saudi Arabia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'si': 'Slovenia',
    'sk': 'Slovakia',
    'th': 'Thailand',
    'tr': 'Turkey',
    'tw': 'Taiwan',
    'ua': 'Ukraine',
    'us': 'United States',
    've': 'Venezuela',
    'za': 'South Africa'
}

# --- Title ---
st.title("🌍 World News Dashboard")
st.write("Stay up to date with the latest headlines by country or keyword.")

# --- User Input ---
col1, col2 = st.columns(2)

with col1:
    # Convert country codes to display names for selection
    country_names = [f"{name} ({code})" for code, name in COUNTRIES.items()]
    selected_country = st.selectbox("Select a country", country_names)
    # Extract country code from selection
    country_code = selected_country.split('(')[-1].strip(')')

with col2:
    # Date selection
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    start_date = st.date_input("From date", week_ago)
    end_date = st.date_input("To date", today)

keyword = st.text_input("Search by keyword (optional):", "")

# --- API Request ---
params = {
    "apiKey": API_KEY,
    "country": country_code if not keyword else "",
    "q": keyword if keyword else "",
    "pageSize": 10,
    "from": start_date,
    "to": end_date
}

if st.button("Fetch News"):
    # Validate date range
    if start_date > end_date:
        st.error("Error: End date must be after start date.")
    else:
        with st.spinner("Fetching news..."):
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get("articles", [])

                if articles:
                    st.subheader(f"📰 Top Headlines for {COUNTRIES[country_code]} from {start_date} to {end_date}")
                    for article in articles:
                        st.markdown(f"### [{article['title']}]({article['url']})")
                        st.write(article['description'])
                        published_date = article['publishedAt'][:10]  # Extract YYYY-MM-DD
                        st.caption(f"Source: {article['source']['name']} | Published: {published_date}")
                        st.write("---")
                else:
                    st.info("No articles found for the selected criteria.")
            else:
                st.error(f"API Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
