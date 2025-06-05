import streamlit as st
import requests
from datetime import datetime

# NewsAPI Configuration
API_KEY = "e8f7788e76b24e45b9f7e57cbb6130f5"  # Replace with your key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Complete country list including Palestine (ps) and excluding Israel (il)
COUNTRIES = {
    'ae': '🇦🇪 UAE', 'ar': '🇦🇷 Argentina', 'at': '🇦🇹 Austria', 
    'au': '🇦🇺 Australia', 'be': '🇧🇪 Belgium', 'bg': '🇧🇬 Bulgaria',
    'br': '🇧🇷 Brazil', 'ca': '🇨🇦 Canada', 'ch': '🇨🇭 Switzerland',
    'cn': '🇨🇳 China', 'co': '🇨🇴 Colombia', 'cu': '🇨🇺 Cuba',
    'cz': '🇨🇿 Czechia', 'de': '🇩🇪 Germany', 'eg': '🇪🇬 Egypt',
    'fr': '🇫🇷 France', 'gb': '🇬🇧 UK', 'gr': '🇬🇷 Greece',
    'hk': '🇭🇰 Hong Kong', 'hu': '🇭🇺 Hungary', 'id': '🇮🇩 Indonesia',
    'ie': '🇮🇪 Ireland', 'in': '🇮🇳 India', 'it': '🇮🇹 Italy',
    'jp': '🇯🇵 Japan', 'kr': '🇰🇷 Korea', 'lt': '🇱🇹 Lithuania',
    'lv': '🇱🇻 Latvia', 'ma': '🇲🇦 Morocco', 'mx': '🇲🇽 Mexico',
    'my': '🇲🇾 Malaysia', 'ng': '🇳🇬 Nigeria', 'nl': '🇳🇱 Netherlands',
    'no': '🇳🇴 Norway', 'nz': '🇳🇿 New Zealand', 'ph': '🇵🇭 Philippines',
    'pl': '🇵🇱 Poland', 'ps': '🇵🇸 Palestine', 'pt': '🇵🇹 Portugal',
    'ro': '🇷🇴 Romania', 'rs': '🇷🇸 Serbia', 'ru': '🇷🇺 Russia',
    'sa': '🇸🇦 Saudi Arabia', 'se': '🇸🇪 Sweden', 'sg': '🇸🇬 Singapore',
    'si': '🇸🇮 Slovenia', 'sk': '🇸🇰 Slovakia', 'th': '🇹🇭 Thailand',
    'tr': '🇹🇷 Turkey', 'tw': '🇹🇼 Taiwan', 'ua': '🇺🇦 Ukraine',
    'us': '🇺🇸 USA', 've': '🇻🇪 Venezuela', 'za': '🇿🇦 South Africa'
}

# Streamlit App
st.set_page_config(page_title="World News Dashboard", layout="wide")
st.title("🌍 World News Dashboard")
st.write("Get all news headlines by country and date")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    selected_country = st.selectbox(
        "Select Country",
        options=list(COUNTRIES.values()),
        index=list(COUNTRIES.values()).index('🇺🇸 USA')
    )
    country_code = [k for k, v in COUNTRIES.items() if v == selected_country][0]

with col2:
    selected_date = st.date_input(
        "Select Date",
        datetime.now()
    )

# Fetch and Display News
if st.button("Get Daily News", type="primary"):
    with st.spinner(f"Fetching news for {selected_country} on {selected_date}..."):
        try:
            # Get recent news (NewsAPI's top-headlines doesn't support historical dates)
            response = requests.get(
                BASE_URL,
                params={
                    "apiKey": API_KEY,
                    "country": country_code,
                    "pageSize": 100  # Max results for free tier
                }
            )
            response.raise_for_status()
            
            # Filter articles by selected date
            all_articles = response.json().get('articles', [])
            daily_news = [
                article for article in all_articles 
                if article['publishedAt'].startswith(str(selected_date))
            ]
            
            # Display results
            if not daily_news:
                st.warning(f"No news found for {selected_country} on {selected_date}")
                st.info("Note: Free NewsAPI only shows very recent news (last 1-2 days)")
            else:
                st.success(f"📰 Found {len(daily_news)} news articles")
                
                for article in daily_news:
                    with st.expander(f"**{article['title']}**", expanded=False):
                        st.write(article.get('description', 'No description available'))
                        st.caption(f"**Source:** {article['source']['name']} | **Published:** {article['publishedAt'][11:16]} UTC")
                        st.markdown(f"[Read full article →]({article['url']})")
                        st.divider()
                        
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
