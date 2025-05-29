import streamlit as st
import requests

# --- Sidebar Menu ---
menu = st.sidebar.selectbox("Select a page", ["Home", "Currency Exchange"])

# --- Home Page ---
if menu == "Home":
    st.title("Made by Rui 👋")
    st.write("Welcome to Rui's Streamlit app!")

    # Text input
    widgetuser_input = st.text_input("Enter a custom message:", "Hello, Siuuuu!")
    st.write("Customized Message:", widgetuser_input)

# --- Currency Exchange Page ---
elif menu == "Currency Exchange":
    st.title("💱 Currency Exchange Tool")

    # Get supported currencies from API
    currencies_response = requests.get("https://api.vatcomply.com/currencies")
    if currencies_response.status_code == 200:
        currencies = currencies_response.json()
        currency_list = sorted(currencies.keys())

        # User input for currency selection
        base_currency = st.selectbox("Base Currency", currency_list, index=currency_list.index("USD"))
        target_currency = st.selectbox("Target Currency", currency_list, index=currency_list.index("MYR"))
        amount = st.number_input(f"Amount in {base_currency}", min_value=0.0, value=1.0)

        # Fetch exchange rate
        rate_response = requests.get(f"https://api.vatcomply.com/rates?base={base_currency}")
        if rate_response.status_code == 200:
            rate_data = rate_response.json()
            rate = rate_data["rates"].get(target_currency)

            if rate:
                converted = amount * rate
                st.success(f"{amount:.2f} {base_currency} = {converted:.2f} {target_currency}")
                st.caption(f"Exchange Rate: 1 {base_currency} = {rate:.4f} {target_currency}")
            else:
                st.error(f"Exchange rate for {target_currency} not found.")
        else:
            st.error(f"Failed to fetch exchange rates: {rate_response.status_code}")
    else:
        st.error("Failed to load currency list.")


