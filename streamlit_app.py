import streamlit as st
import requests
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

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
        value=(18, 21)  # Default: 18th-21st century
    
    st.markdown("""
    **Data Sources**:
    - [On This Day API](https://byabbe.se/on-this-day/)
    - [Wikipedia Events](https://en.wikipedia.org)
    """)

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
    
    return sorted(events, key=lambda x: int(x.get("year", 0)), reverse=True)

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
            if min_century <= (int(e["year"]) // 100 + 1) <= max_century
        ]
        
        # --- Display Results ---
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader(f"🗓️ {selected_date.strftime('%B %d')} in History")
            
            for event in filtered_events[:50]:  # Limit to 50 events
                with st.expander(f"**{event['year']}**: {event['description'][:100]}...", expanded=False):
                    st.write(event["description"])
                    if "wikipedia" in event:
                        st.markdown(f"[Read more on Wikipedia]({event['wikipedia'][0]['wikipedia']})")
        
        with col2:
            # --- Visualization ---
            st.subheader("📊 Timeline Analysis")
            
            # Prepare data for visualization
            df = pd.DataFrame(filtered_events)
            df["year"] = df["year"].astype(int)
            df["century"] = (df["year"] // 100) + 1
            
            # Century Distribution
            fig1, ax1 = plt.subplots()
            df["century"].value_counts().sort_index().plot(
                kind="bar", 
                color="teal",
                ax=ax1
            )
            ax1.set_title("Events by Century")
            ax1.set_xlabel("Century")
            ax1.set_ylabel("Count")
            st.pyplot(fig1)
            
            # Year Distribution
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            df.plot.scatter(
                x="year",
                y=[0]*len(df),
                s=100,
                alpha=0.5,
                ax=ax2
            )
            ax2.set_title("Event Timeline")
            ax2.get_yaxis().set_visible(False)
            st.pyplot(fig2)

# --- Footer ---
st.markdown("---")
st.caption("ℹ️ Data sources may have limitations for very ancient dates")
