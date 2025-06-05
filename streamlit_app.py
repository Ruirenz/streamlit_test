import streamlit as st
import requests
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

# --- App Layout ---
st.title("🌍 Daily World News")
st.write("Get all news headlines by country for a specific day")

# --- User Input ---
col1, col2 = st.columns(2)

with col1:
    country_name = st.selectbox(
        "Select country",
        [f"{name} ({code})" for code, name in COUNTRIES.items()]
    )
    country_code = country_name.split('(')[-1].strip(')')

with col2:
    news_date = st.date_input(
        "Select date",
        datetime.now()
    )

# --- Fetch News ---
if st.button("Get News"):
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "pageSize": 100  # Max allowed by free tier
    }

    with st.spinner(f"Fetching news for {COUNTRIES[country_code]} on {news_date}..."):
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            
            # Filter articles by selected date
            daily_news = [
                article for article in articles 
                if article['publishedAt'].startswith(str(news_date))
            ]

            if daily_news:
                st.subheader(f"🗞️ {len(daily_news)} News for {COUNTRIES[country_code]} on {news_date}")
                
                for article in daily_news:
                    st.markdown(f"### {article['title']}")
                    st.write(article.get('description', ''))
                    st.markdown(f"[Read more]({article['url']})")
                    st.caption(f"Source: {article['source']['name']} | Published: {article['publishedAt'][11:16]}")
                    st.write("---")
            else:
                st.info("No news found for this date. Try a different date or country.")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch news: {e}")
