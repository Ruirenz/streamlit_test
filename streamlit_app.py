import streamlit as st
import requests
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

# ✅ MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide")

# ✅ Custom Background - must come AFTER set_page_config
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1603575448362-cf57b1f696cc?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);  /* Optional overlay */
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Now the rest of your app
st.title("📚 Historical Events Explorer")
st.write("Discover what happened on any date in history")



