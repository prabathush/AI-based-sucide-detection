import streamlit as st
import re
from utils import register_user

def validate_email(email):
    """Validate email format"""
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

def validate_phone(phone):
    """Ensure phone number is digits and has correct length"""
    return phone.isdigit() and len(phone) in [10, 11]  # Example: 10 or 11 digits

def register_page():
    st.title("Create New Account")

    st.markdown("<style>input {font-size: 20px !important;}</style>", unsafe_allow_html=True)

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    date_of_birth = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone_number = st.text_input("Phone Number")

    # Validation flags
    valid = True
    if st.button("Register"):
        # Check if first name is provided
        if not first_name.strip():
            st.error("First Name is required.")
            valid = False

        # Check if last name is provided
        if not last_name.strip():
            st.error("Last Name is required.")
            valid = False

        # Check if username is provided
        if not username.strip():
            st.error("Username is required.")
            valid = False

        # Check if email is valid
        if not email.strip() or not validate_email(email):
            st.error("A valid Email is required.")
            valid = False

        # Check if password is provided and meets length requirement
        if not password.strip() or len(password) < 6:
            st.error("Password is required and must be at least 6 characters long.")
            valid = False

        # Check if phone number is valid
        if not phone_number.strip() or not validate_phone(phone_number):
            st.error("Phone Number must be numeric and contain 10 or 11 digits.")
            valid = False

        # Check if date of birth is provided (date_input always provides a value)
        if not date_of_birth:
            st.error("Date of Birth is required.")
            valid = False

        # If all validations pass, proceed with registration
        if valid:
            if register_user(first_name, last_name, username, email, password, date_of_birth, gender, phone_number):
                st.success("Account created successfully! Please log in.")
                st.session_state.page = 'Login'  # Redirect to Login page
            else:
                st.error("Registration failed. Please try again.")

    if st.button("Already have an account? Login"):
        st.session_state.page = 'Login'  # Redirect to Login page

# Utility function for validation (can be reused)
def validate_email(email):
    """Validate email format"""
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

def validate_phone(phone):
    """Ensure phone number is digits and has correct length"""
    return phone.isdigit() and len(phone) in [10, 11]  # Example: 10 or 11 digits
