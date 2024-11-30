import streamlit as st
import time  # Import time to allow for a delay
from utils import update_profile, get_user_data, deactivate_profile  # Make sure to import the deactivate_profile function

def profile_page():
    if 'user_data' not in st.session_state or not st.session_state.get("logged_in"):
        st.error("Please login to access your profile")
        return

    user_data = st.session_state.user_data

    st.title("Manage Profile")
    new_first_name = st.text_input("First Name", value=user_data['first_name'])
    new_last_name = st.text_input("Last Name", value=user_data['last_name'])
    new_email = st.text_input("Email", value=user_data['email'])
    new_phone_number = st.text_input("Phone Number", value=user_data['phone_number'])

    # Check if the gender is valid; otherwise, default to "Male"
    gender_options = ["Male", "Female", "Other"]
    selected_gender = user_data['gender'] if user_data['gender'] in gender_options else "Male"

    # Selectbox with a default value that is valid
    new_gender = st.selectbox("Gender", gender_options, index=gender_options.index(selected_gender))

    if st.button("Update Profile"):
        # Update the profile in the database
        if update_profile(user_data['id'], new_first_name, new_last_name, new_email, user_data['date_of_birth'], new_gender, new_phone_number):
            st.success("Profile updated successfully")

            # Fetch the updated data from the database and update session state
            st.session_state.user_data = get_user_data(user_data['id'])

        else:
            st.error("Error updating profile")

    # Add a Deactivate Profile section
    st.markdown("---")  # Divider line
    st.subheader("Deactivate Profile")

    # Add a checkbox to confirm deactivation
    confirm = st.checkbox("I confirm that I want to deactivate my profile")

    if confirm:
        # Only show the button if the checkbox is confirmed
        if st.button("Deactivate Profile"):
            # Call deactivate_profile function to remove the user from the system
            if deactivate_profile(user_data['id']):
                st.success("Profile deactivated successfully. You will be logged out shortly.")
                
                # Wait for 2 seconds to show the success message
                time.sleep(2)
                
                # Clear session state and rerun
                st.session_state.logged_in = False
                st.session_state.user_data = None

                # Rerun the app to reflect changes
                st.rerun()
            else:
                st.error("Error deactivating profile")
