import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- Config ---
API_KEY = "e8f7788e76b24e45b9f7e57cbb6130f5"  # Replace with your key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Updated country list with Palestine and without Israel
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
    'ps': 'Palestine',
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
st.write("Get news headlines by country for a specific day")

# --- User Input ---
col1, col2 = st.columns(2)

with col1:
    # Country selection with formatted display
    country_names = [f"{name} ({code})" for code, name in COUNTRIES.items()]
    selected_country = st.selectbox("Select country", country_names, index=0)
    country_code = selected_country.split('(')[-1].strip(')')

with col2:
    # Single date selection (default to today)
    news_date = st.date_input("Select date", datetime.now())

keyword = st.text_input("Filter by keyword (optional):", "")

# --- API Request ---
if st.button("Get News"):
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "q": keyword if keyword else "",
        "pageSize": 100,  # Max allowed by free tier
    }

    with st.spinner(f"Fetching news for {COUNTRIES[country_code]} on {news_date}..."):
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raises exception for 4XX/5XX errors
            
            news_data = response.json()
            articles = news_data.get("articles", [])
            
            # Filter articles by selected date (since API might return recent articles)
            filtered_articles = [
                article for article in articles 
                if article['publishedAt'].startswith(str(news_date))
            ]

            if filtered_articles:
                st.subheader(f"📰 News for {COUNTRIES[country_code]} on {news_date}")
                
                for article in filtered_articles:
                    published_time = article['publishedAt'][11:16]  # Extract HH:MM
                    st.markdown(f"### [{article['title']}]({article['url']})")
                    st.write(article.get('description', 'No description available'))
                    st.caption(f"🕒 {published_time} | 📰 {article['source']['name']}")
                    st.write("---")
                
                st.success(f"Found {len(filtered_articles)} articles")
            else:
                st.info("No articles found for the selected date. Try a more recent date.")
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching news: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
