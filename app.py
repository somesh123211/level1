from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os, random

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)
CORS(app)

# MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

# SendGrid SMTP credentials from .env
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587  # TLS
SMTP_USERNAME = "apikey"  # fixed
SMTP_PASSWORD = os.getenv("SENDGRID_PASSWORD")  # stored in .env

# MongoDB connection
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client["placement_db"]
    students_collection = db["students"]
    otp_collection = db["otp_temp"]
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Error:", e)

# Helper function to send OTP via SMTP
import requests
import os

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_otp_email(email, otp):
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{"to": [{"email": email}]}],
        "from": {"email": "indra656778@gmail.com"},  # your verified sender
        "subject": "Student Placement OTP",
        "content": [{"type": "text/plain", "value": f"Your OTP is: {otp}"}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202:
        print("OTP sent successfully to", email)
        return True
    else:
        print("SendGrid Error:", response.status_code, response.text)
        return False


# Home route
@app.route('/')
def home():
    return "Flask + MongoDB Atlas + SendGrid SMTP connected successfully!"

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    branch = data.get("branch")
    email = data.get("email")
    year = data.get("year")

    if not all([name, branch, email, year]):
        return jsonify({"message": "All fields are required"}), 400

    if students_collection.find_one({"email": email}):
        return jsonify({"message": "Email already registered"}), 400

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    if send_otp_email(email, otp):
        # Store OTP temporarily
        otp_collection.update_one(
            {"email": email},
            {"$set": {"otp": otp}},
            upsert=True
        )
        return jsonify({"message": "OTP sent to your email"}), 200
    else:
        return jsonify({"message": "Failed to send OTP"}), 500

# Verify OTP
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    name = data.get("name")
    branch = data.get("branch")
    email = data.get("email")
    year = data.get("year")
    otp_input = data.get("otp")

    if not all([name, branch, email, year, otp_input]):
        return jsonify({"message": "All fields including OTP are required"}), 400

    record = otp_collection.find_one({"email": email})
    if not record or record["otp"] != otp_input:
        return jsonify({"message": "Invalid OTP"}), 400

    # Save student to main collection
    students_collection.insert_one({
        "name": name,
        "branch": branch,
        "email": email,
        "year": year
    })

    # Remove OTP after successful verification
    otp_collection.delete_one({"email": email})
    return jsonify({"message": "Student registered successfully!"}), 200

# Login route (email only)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "Email required"}), 400

    student = students_collection.find_one({"email": email})
    if student:
        return jsonify({"message": f"Welcome {student['name']}!"}), 200
    else:
        return jsonify({"message": "Email not registered"}), 400

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

