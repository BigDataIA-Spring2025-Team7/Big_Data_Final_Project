import streamlit as st
import requests
import json

def show_signup(API_URL):
    st.header("Sign Up")
    signup_username = st.text_input("Username", key="signup_username")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    
    chronic_conditions = ["Heart", "Diabetes", "Asthma", "Headache", "Other"]
    chronic_condition = st.selectbox("Chronic Condition", chronic_conditions)
    
    if chronic_condition == "Other":
        chronic_condition = st.text_input("Please specify your condition")
    
    location = st.text_input("Location")
    
    if st.button("Sign Up"):
        if signup_username and signup_password and chronic_condition and location:
            try:
                payload = {
                    "username": signup_username,
                    "password": signup_password,
                    "chronic_condition": chronic_condition,
                    "location": location
                }
                
                response = requests.post(
                    f"{API_URL}/users/signup",
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("Registration successful! Please login.")
                else:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get("detail", "Registration failed.")
                        st.error(f"Error: {error_msg}")
                    except:
                        st.error(f"Registration failed with status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all fields.")