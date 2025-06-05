import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Config ---
API_KEY = "e8f7788e76b24e45b9f7e57cbb6130f5"  # Replace with your ke
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Updated list of all available countries (including Palestine, excluding Israel)
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
    # Convert country codes to display names for selection
    country_names = [f"{name} ({code})" for code, name in COUNTRIES.items()]
    selected_country = st.selectbox("Select a country", country_names)
    # Extract country code from selection
    country_code = selected_country.split('(')[-1].strip(')')

with col2:
    # Single date selection
    selected_date = st.date_input("Select date", datetime.now())

keyword = st.text_input("Search by keyword (optional):", "")

# --- API Request ---
params = {
    "apiKey": API_KEY,
    "country": country_code,
    "q": keyword if keyword else "",
    "pageSize": 100,  # Maximum allowed by free tier
    "from": selected_date,
    "to": selected_date + timedelta(days=1)  # Include the full selected day
}

if st.button("Fetch News"):
    with st.spinner(f"Fetching news for {COUNTRIES[country_code]} on {selected_date}..."):
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])

            if articles:
                st.subheader(f"📰 News for {COUNTRIES[country_code]} on {selected_date}")
                
                # Convert to DataFrame for better display
                news_df = pd.DataFrame(articles)
                news_df['publishedAt'] = pd.to_datetime(news_df['publishedAt']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Display in a clean table with clickable links
                for idx, row in news_df.iterrows():
                    st.markdown(f"### [{row['title']}]({row['url']})")
                    st.write(row['description'])
                    st.caption(f"Source: {row['source']['name']} | Published: {row['publishedAt']}")
                    st.write("---")
                
                st.success(f"Found {len(articles)} articles")
            else:
                st.info("No articles found for the selected date and country.")
        else:
            error_msg = response.json().get('message', 'Unknown error')
            st.error(f"API Error: {response.status_code} - {error_msg}")
