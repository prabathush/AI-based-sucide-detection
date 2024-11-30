import streamlit as st
from login import login_page
from register import register_page
from profile import profile_page
from suicide_detection import suicide_detection_page
from history import history_page

def main():
    # Initialize session state for login and user data
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'  # Default to Login

    # Navigation based on logged-in status
    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        # Navigation menu with History capitalized for consistency
        page = st.sidebar.selectbox("Go to", ["Suicide Detection", "Profile", "History", "Logout"])

        if page == "Suicide Detection":
            suicide_detection_page()
        elif page == "Profile":
            profile_page()
        elif page == "History":
            history_page()  # Show the history page
        elif page == "Logout":
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.page = 'Login'
            st.experimental_rerun()  # Logout and rerun to show login page
    else:
        # Handle page navigation if not logged in
        if st.session_state.page == 'Login':
            login_page()
        elif st.session_state.page == 'Register':
            register_page()

if __name__ == "__main__":
    main()
