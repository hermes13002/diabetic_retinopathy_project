import sqlite3
import hashlib
from datetime import datetime
 

# Hash Password.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Create Database Connection.
def get_db_connection():
    connection = sqlite3.connect('medical_data.db')
    return connection


# Initialize database.
def init_db():
    connection = get_db_connection()
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                name TEXT,
                hashed_password TEXT,
                email TEXT
            )
        ''')
        connection.commit()
        connection.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                name TEXT,
                age INTEGER,
                gender TEXT,
                contact_info TEXT
            )
        ''')
        connection.commit()
        connection.execute('''
            CREATE TABLE IF NOT EXISTS DR_Prediction (
                prediction_id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                prediction_date TEXT,
                prediction_class TEXT,
                confidence_score REAL,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        connection.commit()
    connection.close()


# Add User Table.
def add_user(username, name, password, email):
    connection = get_db_connection()
    hashed_password = hash_password(password)
    with connection:
        connection.execute('INSERT INTO users (username, name, hashed_password, email) VALUES (?, ?, ?, ?)',
                     (username, name, hashed_password, email))
        connection.commit()
    connection.close()


# Authenticate user.
def authenticate_user(username, password):
    connection = get_db_connection()
    hashed_password = hash_password(password)
    user = connection.execute('SELECT * FROM users WHERE username = ? AND hashed_password = ?', (username, hashed_password)).fetchone()
    connection.commit()
    connection.close()
    return user


# Add Patient Table.
def add_patient(user_name, name, age, gender, contact_info):
    connection = get_db_connection()
    with connection:
        connection.execute('INSERT INTO patients (username, name, age, gender, contact_info) VALUES (?, ?, ?, ?, ?)',
                     (user_name, name, age, gender, contact_info))
        connection.commit()
    connection.close()


# Add Prediction Table.
def add_dr_prediction(patient_id, prediction_class, confidence_score):
    connection = get_db_connection()
    prediction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with connection:
        connection.execute('INSERT INTO DR_Prediction (patient_id, prediction_date, prediction_class, confidence_score) VALUES (?, ?, ?, ?)',
                     (patient_id, prediction_date, prediction_class, confidence_score))
        connection.commit()
    connection.close()
    
    
# Function to get a patient's data from the database.
def get_patient_data(username):
    connection = get_db_connection()
    connection.execute("SELECT name, age, gender, contact FROM patients WHERE username=?", (username,))
    data = connection.fetchone()
    if data:
        return {
            "name": data[0],
            "age": data[1],
            "gender": data[2],
            "contact": data[3]
        }
    return None