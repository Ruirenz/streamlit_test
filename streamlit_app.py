import streamlit as st
import requests
import pandas as pd

# --- Config ---
API_KEY = "your_newsapi_key_here"  # Replace with your key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# --- Title ---
st.title("🌍 World News Dashboard")
st.write("Stay up to date with the latest headlines by country or keyword.")

# --- User Input ---
country = st.selectbox("Select a country", ["us", "gb", "my", "in", "au", "de", "fr", "jp", "sg"])
keyword = st.text_input("Or search by keyword (optional):", "")

# --- API Request ---
params = {
    "apiKey": API_KEY,
    "country": country if not keyword else "",
    "q": keyword if keyword else "",
    "pageSize": 10,
}

if st.button("Fetch News"):
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])

        if articles:
            st.subheader("📰 Top Headlines")
            for article in articles:
                st.markdown(f"### [{article['title']}]({article['url']})")
                st.write(article['description'])
                st.caption(f"Source: {article['source']['name']} | Published: {article['publishedAt']}")
                st.write("---")
        else:
            st.info("No articles found.")
    else:
        st.error(f"API Error: {response.status_code}")
