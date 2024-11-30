import streamlit as st
from utils import login_user

def login_page():
    st.title("Login to Your Account")

    # Larger font for input fields
    st.markdown("<style>input {font-size: 20px !important;}</style>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, user_data = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            st.session_state.page = 'Suicide Detection'  # Redirect to Suicide Detection page
        else:
            st.error("Login failed. Check your credentials.")

    if st.button("Don't have an account? Register"):
        st.session_state.page = 'Register'  # Redirect to Register page
