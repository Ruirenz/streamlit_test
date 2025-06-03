import streamlit as st
from datetime import date

# --- Background Color Styling ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://m.media-amazon.com/images/M/MV5BNzczMzQ3MmItMGFjZC00NzEwLWEzZWYtZTliMjkwOWQ2YzIxXkEyXkFqcGdeQXRyYW5zY29kZS13b3JrZmxvdw@@._V1_.jpg");
        background-repeat: repeat;
        background-size: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
menu = st.sidebar.selectbox("Select a Calculator", [
    "BMI Calculator",
    "Age Calculator",
    "Temperature Converter"
])

# --- BMI Calculator ---
if menu == "BMI Calculator":
    st.title("🏋️ BMI Calculator")
    weight = st.number_input("Enter your weight (kg):", min_value=0.0, value=60.0)
    height = st.number_input("Enter your height (cm):", min_value=0.0, value=170.0)

    if st.button("Calculate BMI"):
        if weight > 0 and height > 0:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"Your BMI is: {bmi:.2f}")
            if bmi < 18.5:
                st.info("Category: Underweight")
            elif bmi < 24.9:
                st.info("Category: Normal weight")
            elif bmi < 29.9:
                st.info("Category: Overweight")
            else:
                st.info("Category: Obese")
        else:
            st.warning("Please enter valid height and weight.")

# --- Age Calculator ---
elif menu == "Age Calculator":
    st.title("🎂 Age Calculator")
    dob = st.date_input("Enter your date of birth:", date(2000, 1, 1))

    if st.button("Calculate Age"):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        st.success(f"You are {age} years old.")

# --- Temperature Converter ---
elif menu == "Temperature Converter":
    st.title("🌡️ Temperature Converter")
    conversion = st.selectbox("Select conversion direction:", [
        "Celsius to Fahrenheit",
        "Fahrenheit to Celsius"
    ])
    temp = st.number_input("Enter temperature value:")

    if st.button("Convert"):
        if conversion == "Celsius to Fahrenheit":
            result = (temp * 9/5) + 32
            st.success(f"{temp}°C = {result:.2f}°F")
        else:
            result = (temp - 32) * 5/9
            st.success(f"{temp}°F = {result:.2f}°C")
