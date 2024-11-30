import streamlit as st
from utils import load_resources, clean_text, insert_feedback, insert_prediction_history
from tensorflow.keras.preprocessing.sequence import pad_sequences
import plotly.express as px

model, tokenizer = load_resources()

def suicide_detection_page():
    st.title("Suicide Detection Application")

    # Custom CSS to make the text bigger
    st.markdown(
        """
        <style>
        textarea {font-size: 20px !important;}
        .stButton>button {font-size: 18px !important;}
        </style>
        """, unsafe_allow_html=True
    )

    # Initialize session state variables
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'prediction_logged' not in st.session_state:
        st.session_state.prediction_logged = False

    # User Input Field
    user_input = st.text_area("Enter your thoughts or feelings here", value=st.session_state.user_input)

    if st.button('Analyze'):
        # Clean and predict
        cleaned_input = clean_text(user_input)
        sequences = tokenizer.texts_to_sequences([cleaned_input])
        padded_sequences = pad_sequences(sequences, maxlen=50)
        prediction = model.predict(padded_sequences)[0][0]

        # Store input and prediction in session state
        st.session_state.user_input = user_input
        st.session_state.prediction = prediction
        st.session_state.prediction_logged = False  # Reset the prediction logging status

    # If a prediction is available, display the results
    if st.session_state.prediction is not None:
        prediction = st.session_state.prediction
        user_input = st.session_state.user_input

        st.subheader('Your Input:')
        st.write(user_input)

        likely_suicidal_thoughts = float(prediction * 100)
        less_likely_suicidal_thoughts = float((1 - prediction) * 100)

        # Show prediction based on threshold
        if prediction > 0.5:
            st.subheader(f'Prediction: {likely_suicidal_thoughts:.2f}% Likely Suicidal Thoughts')
            if likely_suicidal_thoughts > 75:
                st.error("Warning: High probability of suicidal thoughts. Please seek help immediately.")
            elif likely_suicidal_thoughts > 50:
                st.warning("You may be experiencing suicidal thoughts.")
        else:
            st.subheader(f'Prediction: {less_likely_suicidal_thoughts:.2f}% Less Likely Suicidal Thoughts')
            st.success("Your input suggests less likelihood of suicidal thoughts.")

        # Progress bar for confidence
        st.progress(float(prediction))

        # Plot probabilities
        probabilities = {
            'Likely Suicidal Thoughts': likely_suicidal_thoughts,
            'Less Likely Suicidal Thoughts': less_likely_suicidal_thoughts
        }

        fig = px.bar(x=list(probabilities.keys()), y=list(probabilities.values()), 
                     labels={'x': 'Category', 'y': 'Probability (%)'}, title='Prediction Probability')
        st.plotly_chart(fig)

        # Show feedback based on the prediction
        if prediction > 0.5:
            st.error("Warning: Your input suggests you may be experiencing suicidal thoughts.")
        else:
            st.success("Your input suggests less likelihood of suicidal thoughts.")

        # Display additional details
        st.subheader('Details:')
        st.write("This application uses a trained LSTM model to detect whether your current thoughts or feelings may indicate suicidal tendencies. "
                 "The model was trained on a dataset of text inputs using GloVe embeddings for word representations.")

        # Enhanced Summary
        st.subheader('Summary:')
        st.write(f"**Likely Suicidal Thoughts**: {likely_suicidal_thoughts:.2f}%")
        st.write(f"**Less Likely Suicidal Thoughts**: {less_likely_suicidal_thoughts:.2f}%")

        # Additional Supportive Message
        if prediction > 0.5:
            st.warning("You are not alone, and help is available. Please reach out to someone you trust or contact a helpline.")
            st.markdown("[Find Help Now](https://www.suicidepreventionlifeline.org)")
        else:
            st.info("Keep taking care of your mental health and stay connected with loved ones.")

        # User Feedback
        st.subheader("Was this prediction accurate?")
        feedback_type = st.radio("How do you feel about this prediction?", ("Very Accurate", "Somewhat Accurate", "Not Accurate"))
        if st.button("Submit Feedback"):
            # Insert feedback into the database
            user_id = st.session_state.user_data['id'] if 'user_data' in st.session_state else None
            insert_feedback(user_id, feedback_type, user_input, float(prediction))
            st.session_state.feedback = feedback_type
            st.success("Thank you for your feedback!")

        # Only insert prediction history if it hasn't been logged yet
        if not st.session_state.prediction_logged and st.session_state.logged_in:
            user_id = st.session_state.user_data['id']
            insert_prediction_history(user_id, user_input, float(prediction))
            st.session_state.prediction_logged = True  # Mark as logged to prevent re-insertions
