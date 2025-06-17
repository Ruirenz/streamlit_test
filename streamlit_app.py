import streamlit as st
import requests
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

# --- Custom Background from Web ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.unsplash.com/photo-1603575448362-cf57b1f696cc?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    .block-container {{
        background-color: rgba(0, 0, 0, 0.6);  /* Dark overlay */
        padding: 2rem;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("📚 Historical Events Explorer")
st.write("Discover what happened on any date in history")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("Filters")
    selected_date = st.date_input(
        "Select Date",
        value=date(1969, 7, 20),
        min_value=date(1, 1, 1),
        max_value=date.today()
    )

    year_filter = st.slider(
        "Filter by Century",
        min_value=1,
        max_value=21,
        value=(18, 21)
    )

    st.markdown("""**Data Sources**:
    - [On This Day API](https://byabbe.se/on-this-day/)
    - [Wikipedia Events](https://en.wikipedia.org)""")

# --- API Functions ---
def fetch_wikipedia_events(month, day):
    """Get events from Wikipedia's 'On This Day' API"""
    url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json().get("events", [])
    except:
        return []
    return []

def fetch_historical_events(month, day, year=None):
    """Combine multiple data sources"""
    events = fetch_wikipedia_events(month, day)

    # Filter by year if provided
    if year:
        events = [e for e in events if str(year) in e.get("year", "")]

    # Safely convert year to int and filter invalid entries
    valid_events = []
    for e in events:
        try:
            e["year"] = int(e["year"])
            valid_events.append(e)
        except (ValueError, TypeError):
            continue

    return sorted(valid_events, key=lambda x: x["year"], reverse=True)

# --- Main Display ---
if st.button("🔍 Find Historical Events"):
    month, day, year = selected_date.month, selected_date.day, selected_date.year
    events = fetch_historical_events(month, day)

    if not events:
        st.warning("No events found for this date")
    else:
        # Apply century filter
        min_century, max_century = year_filter
        filtered_events = [
            e for e in events 
            if min_century <= (e["year"] // 100 + 1) <= max_century
        ]

        # --- Display Results ---
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader(f"🗓️ {selected_date.strftime('%B %d')} in History")

            for event in filtered_events[:50]:  # Limit to 50 events
                with st.expander(f"**{event['year']}**: {event['description'][:100]}...", expanded=False):
                    st.write(event["description"])
                    if "wikipedia" in event and event["wikipedia"]:
                        st.markdown(f"[Read more on Wikipedia]({event['wikipedia'][0]['wikipedia']})")

        with col2:
            # --- Visualization ---
            st.subheader("📊 Timeline Analysis")

            # Prepare data for visualization
            df = pd.DataFrame(filtered_events)
            df["century"] = (df["year"] // 100) + 1


