import mysql.connector
import bcrypt
from tensorflow.keras.models import load_model
import pickle
import re
import streamlit as st
import nltk
import mysql.connector
from mysql.connector import Error
from nltk.corpus import stopwords

# Download stopwords from NLTK (run once if not already downloaded)
nltk.download('stopwords')

# Initialize stop words from NLTK
stop_words = set(stopwords.words('english'))

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="suicide_detection"
    )

# Function to handle user login
def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return True, user
        return False, None
    finally:
        cursor.close()
        conn.close()

def register_user(first_name, last_name, username, email, password, date_of_birth, gender, phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("""
            INSERT INTO users (first_name, last_name, username, email, password_hash, date_of_birth, gender, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, username, email, hashed_password, date_of_birth, gender, phone_number))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Error during registration: {e}")  # Log the error
        return False
    finally:
        cursor.close()
        conn.close()


# Function to update user profile
def update_profile(user_id, first_name, last_name, email, date_of_birth, gender, phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users SET first_name = %s, last_name = %s, email = %s, date_of_birth = %s, gender = %s, phone_number = %s WHERE id = %s
        """, (first_name, last_name, email, date_of_birth, gender, phone_number, user_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

# Load model and tokenizer using Streamlit's caching mechanism
@st.cache_resource
def load_resources():
    model = load_model('suicide_detection_model.h5')
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return model, tokenizer

# Clean text function for input preprocessing
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words
    return ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="",  # Change to your MySQL password
        database="suicide_detection"
    )

def insert_feedback(user_id, feedback_type, user_input, prediction):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO feedback (user_id, feedback_type, user_input, prediction)
            VALUES (%s, %s, %s, %s)
        """, (user_id, feedback_type, user_input, prediction))
        conn.commit()
    except Error as e:
        print("Error occurred during feedback insertion:", e)
    finally:
        cursor.close()
        conn.close()
        
        
        # Add this function to fetch user data
def get_user_data(user_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch user data from the database based on the user ID
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        return user_data
    except Error as e:
        print("Error fetching user data:", e)
        return None
    finally:
        cursor.close()
        conn.close()
        
        
def get_user_history(user_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT input_text, prediction, prediction_date
            FROM prediction_history
            WHERE user_id = %s
            ORDER BY prediction_date DESC
        """, (user_id,))
        history = cursor.fetchall()
        return history
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def insert_prediction_history(user_id, input_text, prediction):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO prediction_history (user_id, input_text, prediction, prediction_date)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, input_text, prediction))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error inserting prediction history: {e}")
    finally:
        cursor.close()
        conn.close()
        
def get_prediction_history(user_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT input_text, prediction, prediction_date 
            FROM prediction_history 
            WHERE user_id = %s ORDER BY prediction_date DESC
        """, (user_id,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Error fetching history: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def deactivate_profile(user_id):
    conn = create_connection()  # Assuming create_connection() is your function to connect to the DB
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM users 
            WHERE id = %s
        """, (user_id,))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Error deactivating profile: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
