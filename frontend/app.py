import streamlit as st
import requests
from utils.login import show_login
from utils.signup import show_signup
from utils.dashboard import show_dashboard

# Configure the API URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Chronic Disease Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.username = None

# Make sure the default navigation is Dashboard
if "nav_selection" not in st.session_state and st.session_state.token is not None:
    st.session_state.nav_selection = "Dashboard"

st.title("Chronic Disease Management Platform")

# Show different UI based on authentication status
if st.session_state.token is None:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        show_login(API_URL)
    
    with tab2:
        show_signup(API_URL)
else:
    # User is logged in, show dashboard
    show_dashboard(API_URL)