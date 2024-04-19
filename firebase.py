import firebase_admin
from firebase_admin import credentials, db
import os

# Flag to track if Firebase has been initialized
firebase_initialized = False

# Initialize Firebase Admin SDK with the credentials JSON file and database URL
def initialize_firebase():
    global firebase_initialized
    if not firebase_initialized:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_directory, "ath-key.json")
        cred = credentials.Certificate(json_file_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://atherton-marketing-default-rtdb.firebaseio.com/'
        })
        firebase_initialized = True

# Get a reference to the root of your database
def get_database_reference():
    initialize_firebase()  # Make sure Firebase is initialized
    ref = db.reference()
    return ref

# Retrieve user data
def get_user_data(user_id):
    ref = get_database_reference()
    user_ref = ref.child('users').child(user_id)
    user_data = user_ref.get()
    return user_data

def get_all_data():
    ref = get_database_reference()
    user_ref = ref.child('users')
    user_data = user_ref.get()
    return user_data

# Update user data in the database
def update_user_data(update_data):
    ref = get_database_reference()
    user_ref = ref.child('users')
    user_ref.update(update_data)
    return f"User data updated successfully."
