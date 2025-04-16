import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import random
import json

def show_dashboard(API_URL):
    # Initialize navigation selection in session state if not already set
    if "nav_selection" not in st.session_state:
        st.session_state.nav_selection = "Dashboard"
    
    # Add sidebar navigation with only Dashboard and Profile
    with st.sidebar:
        # Show logged in user
        st.success(f"Logged in as: {st.session_state.username}")
        
        # Navigation buttons with default selection from session state
        # Only Dashboard and Profile options
        selected = st.radio(
            "Navigation",
            ["Dashboard", "Profile"],
            index=["Dashboard", "Profile"].index(st.session_state.nav_selection)
        )
        
        # Update session state when selection changes
        st.session_state.nav_selection = selected
        
        # Logout button
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            if "nav_selection" in st.session_state:
                del st.session_state.nav_selection
            st.rerun()
    
    # Display the selected page
    if selected == "Dashboard":
        show_main_home(API_URL)
    elif selected == "Profile":
        show_profile(API_URL)

def show_main_home(API_URL):
    st.header("Home")
    
    # Project summary content
    st.markdown("""
    ## ChronicCare.AI: AI-Powered Health Management System
    
    Chronic health conditions such as Type 2 Diabetes, Hypertension, High Cholesterol, and Heart Disease are on the rise globally, significantly impacting quality of life and healthcare systems. Managing these conditions requires consistent monitoring of diet, medication, and access to real-time medical updates.
    
    **ChronicCare.AI** is an AI-powered, patient-centric health management system that empowers individuals with chronic conditions to take control of their health. By integrating structured nutrition and medication data, unstructured health literature (PDFs, articles), location-based services, and AI-driven insights from large language models, the platform offers a unified experience for dietary guidance, medication adherence, and real-time medication updates.
    
    ### The Challenge
    
    Managing chronic illnesses is a complex and often overwhelming task. Patients must juggle multiple variables such as diet restrictions, medication schedules, etc.
    
    Despite the abundance of medical knowledge and digital health tools, there is **no centralized system** that:
    * Provides personalized nutrition, medication, and lifestyle guidance based on the user's condition.
    * Integrates real-time health insights with condition-specific recommendations.
    * Supports proactive alerts, and community/hospital discovery.
    
    The lack of personalization, integration, and proactive support leads to **non-adherence, misinformation, and worsening health outcomes**.
    
    ### Goals & Objectives
    
    The goal of **ChronicCare.AI** is to design an intelligent assistant that supports end-to-end chronic disease management, leveraging structured data, unstructured documents, and AI agents.
    
    **Key Objectives:**
    * To build a **nutritionist module** that provides daily caloric needs and food recommendations based on chronic conditions, with alerting systems for threshold violations through email.
    * To develop a **knowledge base** powered by vector search Pinecone for patient-facing FAQs from research papers, PDFs, and government health guidelines.
    * To integrate with **location-aware web agents** for discovering hospitals, clinics, and support groups nearby.
    * To manage **medication adherence** and provide drug-specific guidance using OpenFDA and RxNorm.
    * To support **mental health journaling** and insights.
    * To deliver **real-time news, discoveries, and research updates** for each condition via web search and summarization.
    """)

def show_profile(API_URL):
    st.header("Profile")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_URL}/users/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("User Information")
                st.write(f"**Username:** {user_data['username']}")
                st.write(f"**Location:** {user_data['location']}")
            
            with col2:
                st.subheader("Medical Information")
                st.write(f"**Chronic Condition:** {user_data['chronic_condition']}")
            
            # Account settings
            st.subheader("Account Settings")
            
            # Simulated settings
            notifications = st.checkbox("Enable Notifications", value=True)
            data_sharing = st.checkbox("Share Anonymous Data for Research", value=False)
            
            if st.button("Update Settings"):
                st.success("Settings updated successfully!")
            
            # Change password
            st.subheader("Change Password")
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                submit_button = st.form_submit_button("Change Password")
                
                if submit_button:
                    if not current_password or not new_password or not confirm_password:
                        st.warning("Please fill all password fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    else:
                        # Send password change request to the backend
                        try:
                            password_data = {
                                "current_password": current_password,
                                "new_password": new_password
                            }
                            
                            change_pw_response = requests.post(
                                f"{API_URL}/users/change-password",
                                json=password_data,
                                headers=headers
                            )
                            
                            if change_pw_response.status_code == 200:
                                st.success("Password changed successfully! Please log in with your new password.")
                                # Clear token to force re-login
                                st.session_state.token = None
                                st.session_state.username = None
                                st.rerun()
                            else:
                                error_msg = "Failed to change password"
                                try:
                                    # Try to get more detailed error message from response
                                    error_data = change_pw_response.json()
                                    if "detail" in error_data:
                                        error_msg = error_data["detail"]
                                except:
                                    pass
                                st.error(f"Error: {error_msg}")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
        else:
            st.error(f"Failed to load user data. Status: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")