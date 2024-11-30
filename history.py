import streamlit as st
from utils import get_prediction_history

def history_page():
    if 'user_data' not in st.session_state or not st.session_state.get("logged_in"):
        st.error("Please login to view your history.")
        return

    user_id = st.session_state.user_data['id']

    st.title("Prediction History")
    
    # Fetch the history from the database
    history_data = get_prediction_history(user_id)
    
    if history_data:
        for entry in history_data:
            st.subheader(f"Prediction Date: {entry['prediction_date']}")
            st.write(f"Input Text: {entry['input_text']}")
            st.write(f"Prediction: {entry['prediction'] * 100:.2f}%")
            st.write("---")
    else:
        st.write("No history found.")
