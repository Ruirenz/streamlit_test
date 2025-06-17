import streamlit as st
import requests
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd


st.set_page_config(layout="wide")


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fillustrations%2Fhistory-lesson&psig=AOvVaw22FSOKIXa28p7lbaSozgEC&ust=1750258210473000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOia0Y3a-I0DFQAAAAAdAAAAABAE");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("📚 Historical Events Explorer")
st.write("Discover what happened on any date in history")


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

# api
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


    if year:
        events = [e for e in events if str(year) in e.get("year", "")]

   
    valid_events = []
    for e in events:
        try:
            e["year"] = int(e["year"])
            valid_events.append(e)
        except (ValueError, TypeError):
            continue

    return sorted(valid_events, key=lambda x: x["year"], reverse=True)


if st.button("🔍 Find Historical Events"):
    month, day, year = selected_date.month, selected_date.day, selected_date.year
    events = fetch_historical_events(month, day)

    if not events:
        st.warning("No events found for this date")
    else:
    
        min_century, max_century = year_filter
        filtered_events = [
            e for e in events 
            if min_century <= (e["year"] // 100 + 1) <= max_century
        ]


        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader(f"🗓️ {selected_date.strftime('%B %d')} in History")

            for event in filtered_events[:50]:  # Limit to 50 events
                with st.expander(f"**{event['year']}**: {event['description'][:100]}...", expanded=False):
                    st.write(event["description"])
                    if "wikipedia" in event and event["wikipedia"]:
                        st.markdown(f"[Read more on Wikipedia]({event['wikipedia'][0]['wikipedia']})")

        with col2:
          
            st.subheader("📊 Timeline Analysis")

          
            df = pd.DataFrame(filtered_events)
            df["century"] = (df["year"] // 100) + 1

           
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

       
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            df['y_value'] = 0
            df.plot.scatter(
                x="year",
                y="y_value",
                s=100,
                alpha=0.5,
                ax=ax2
            )
            ax2.set_title("Event Timeline")
            ax2.get_yaxis().set_visible(False)
            ax2.set_xlabel("Year")
            st.pyplot(fig2)


st.markdown("---")
st.caption("ℹ️ Data sources may have limitations for very ancient dates.")


