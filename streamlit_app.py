import streamlit as st 
import requests

# Set the app title 
st.title('                         __        __              _ 
    ____ ___  ____ _____/ /__     / /_  __  __   _______  __(_)
  / __ `__ \/ __ `/ __  / _ \   / __ \/ / / /  / ___/ / / / / 
 / / / / / / /_/ / /_/ /  __/  / /_/ / /_/ /  / /  / /_/ / /  
/_/ /_/ /_/\__,_/\__,_/\___/  /_.___/\__, /  /_/   \__,_/_/   
                                    /____/                     ') 

# Add a welcome message 
st.write('Welcome to rui Streamlit app!') 

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello,  Siuuuu!') 

# Display the customized message 
st.write('Customized Message:', widgetuser_input)


#API calls
response = requests.get('https://api.vatcomply.com/rates?base=USD')

if response.status_code == 200:
    data = response.json()
    st.write('Output:')
    st.json(data)  # nicely formatted JSON output
else:
    st.error(f"API call failed with status code: {response.status_code}")


