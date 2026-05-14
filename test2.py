import os
import sqlite3
import pickle
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- BUG 1: Hardcoded Secret Key ---
# CodeRabbit will flag this as a major security risk
SECRET_KEY = "super_secret_password_123!"

# --- BUG 2: SQL Injection Vulnerability ---
# Using f-strings to insert user input directly into SQL queries
def get_user_data(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query) # VULNERABLE
    return cursor.fetchall()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # --- BUG 3: Broken Access Control/Logic Error ---
    # Allowing 'admin' login without password verification
    if username == "admin":
        return jsonify({"status": "success", "message": "Admin logged in"}), 200

    user = get_user_data(username)
    if user and user[0][2] == password:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "fail"}), 401

# --- BUG 4: Insecure Deserialization ---
# Accepting base64 encoded pickle data from user input
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_data_base64 = request.form.get('data')
    if user_data_base64:
        # pickle.loads() is highly dangerous on untrusted data
        data = pickle.loads(base64.b64decode(user_data_base64)) # VULNERABLE
        return jsonify({"status": "updated", "data": str(data)})
    return "No data", 400

# --- BUG 5: Improper Error Handling ---
# Exposing full traceback to user
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # --- BUG 6: Debug Mode Active in Production ---
    app.run(debug=True, host='0.0.0.0', port=5000)

