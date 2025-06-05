import streamlit as st
import requests
from datetime import date
import matplotlib.pyplot as plt

st.title("📚 Historical Events Explorer")
st.write("Select any date and explore what happened in history on that day!")

# --- Date Input ---
selected_date = st.date_input("Choose a date", date.today())
month = selected_date.month
day = selected_date.day

# --- API Call ---
if st.button("Show Historical Events"):
    with st.spinner("Fetching data..."):
        url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            events = data.get("events", [])

            if events:
                st.subheader(f"🗓️ Notable Events on {selected_date.strftime('%B %d')}")
                for event in events[:10]:  # show only top 10
                    year = event.get("year")
                    desc = event.get("description")
                    st.markdown(f"- **{year}**: {desc}")
            else:
                st.info("No events found for this date.")

        else:
            st.error("Failed to fetch events. Try again later.")

# --- Optional: Visualize Events by Century ---
    if events:
        st.subheader("📊 Event Count by Century")
        centuries = []
        for event in events:
            try:
                yr = int(event["year"])
                century = (yr // 100 + 1) if yr > 0 else (yr // 100)
                centuries.append(f"{century}th century")
            except:
                continue

        # Plot bar chart
        from collections import Counter
        century_counts = Counter(centuries)
        fig, ax = plt.subplots()
        ax.bar(century_counts.keys(), century_counts.values(), color="skyblue")
        plt.xticks(rotation=45)
        ax.set_ylabel("Number of Events")
        ax.set_title("Events by Century")
        st.pyplot(fig)
