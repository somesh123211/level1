# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from dotenv import load_dotenv
import jwt
import datetime
import os
import re
import json
import google.generativeai as genai
from branch_quiz_ai import quiz_topics
from werkzeug.utils import secure_filename
import os
from bson import ObjectId
import base64
from bson.binary import Binary
from functools import wraps



# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey123")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not MONGO_URI:
    raise Exception("MONGO_URI not set in .env")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY not set in .env")

# -----------------------------
# Configure Google AI (Gemini)
# -----------------------------
genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------
# Flask app setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app, supports_credentials=True)

# -----------------------------
# MongoDB connection
# -----------------------------
client = MongoClient(MONGO_URI)
db = client['placement_portal_v2']
students_collection = db['students']
quiz_collection = db['quiz_results']
branchquiz = db['branchquiz']
quiz_results = db['quiz_results']

# -----------------------------
# Helper — Token validation
# -----------------------------
# Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            token = bearer.split(" ")[1] if " " in bearer else bearer
        if not token:
            return jsonify({"success": False, "error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = students_collection.find_one({"uid_number": data['uid_number']})
            if not current_user:
                return jsonify({"success": False, "error": "Invalid token"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "error": "Token expired"}), 401
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# -----------------------------
# Generate Questions via Google AI
# -----------------------------
def generate_questions(quiz_type: str):
    prompt = f"""
    Generate 10 {quiz_type} multiple-choice questions in JSON array:
    [
      {{
        "question": "Q text",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "answer": "A"
      }}
    ]
    Only valid JSON output. No markdown, no code fences, only JSON array.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
        questions = json.loads(text)

        # Ensure it is always a list
        if isinstance(questions, dict):
            questions = [questions]
        elif not isinstance(questions, list):
            questions = []

        return questions
    except Exception as e:
        print("Google AI API error:", e)
        return []

# -----------------------------
# Signup
# -----------------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ['name', 'uid_number', 'branch', 'year', 'email', 'password', 'confirm_password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400
    if data['password'] != data['confirm_password']:
        return jsonify({"message": "Passwords do not match"}), 400
    if students_collection.find_one({"email": data['email']}):
        return jsonify({"message": "Email already registered"}), 400
    if students_collection.find_one({"uid_number": data['uid_number']}):
        return jsonify({"message": "UID already registered"}), 400

    hashed_password = generate_password_hash(data['password'])
    student = {
        "name": data['name'],
        "uid_number": data['uid_number'],
        "branch": data['branch'],
        "year": data['year'],
        "email": data['email'],
        "password": hashed_password
    }
    students_collection.insert_one(student)
    return jsonify({"message": "Signup successful"}), 200

# -----------------------------
# Login — Generate JWT
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    student = students_collection.find_one({"email": email})
    if not student or not check_password_hash(student['password'], password):
        return jsonify({"message": "Invalid credentials"}), 401
    token = jwt.encode({
        'uid_number': student['uid_number'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm="HS256")
    return jsonify({
        "message": "Login successful",
        "token": token,
        "student_data": {
            "id": str(student['_id']),
            "name": student['name'],
            "email": student['email'],
            "uid_number": student['uid_number'],
            "branch": student.get("branch", "Unknown"),
            "year": student.get("year", "")
        }
    }), 200

# -----------------------------
# Start Quiz — requires JWT
# -----------------------------
@app.route('/start_quiz/<quiz_type>', methods=['GET'])
@token_required
def start_quiz(current_user, quiz_type):
    uid_number = current_user['uid_number']
    questions = generate_questions(quiz_type)
    if not questions:
        return jsonify({"success": False, "error": "Failed to generate quiz"}), 400
    return jsonify({
        "success": True,
        "student": {
            "uid_number": current_user['uid_number'],
            "name": current_user['name'],
            "email": current_user['email']
        },
        "questions": questions
    }), 200

# -----------------------------
# Submit Quiz
# -----------------------------

@app.route("/submit_quiz", methods=["POST"])
@token_required
def submit_quiz(current_user):
    data = request.get_json()
    quiz_type = data.get("quiz_type")
    score = data.get("score")
    total = data.get("total")

    if quiz_type is None or score is None or total is None:
        return jsonify({"error": "quiz_type, score, and total are required"}), 400

    # Save to DB
    result = {
        "uid_number": current_user['uid_number'],
        "quiz_type": quiz_type,
        "score": score,
        "total": total,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    quiz_collection.insert_one(result)

    return jsonify({"success": True, "message": "Quiz submitted successfully"}), 200



# ----------------------------- Branch Quiz Section -----------------------------
branchquiz_collection = db['branchquiz']
# ----------------------------- Start Branch Quiz (Level-wise) -----------------------------
@app.route("/start_branch_quiz", methods=["GET"])
@token_required
def start_branch_quiz(current_user):
    branch = current_user.get("branch", "").strip()
    if not branch or branch.lower() == "unknown":
        return jsonify({"success": False, "error": "Branch information missing. Please update your profile."}), 400

    # Fetch current level of the student (default to 1)
    current_level = current_user.get("current_level", 1)

    # Get topics for this branch and level from branch_quiz_ai.py
    if branch not in quiz_topics:
        return jsonify({"success": False, "error": "Branch not available"}), 400

    level_topics = quiz_topics[branch].get(current_level)
    if not level_topics:
        return jsonify({"success": False, "error": f"No topics defined for level {current_level}"}), 400

    # Build prompt for AI
    prompt_text = f"Generate 10 multiple-choice questions for the {branch} branch on the following topics: {', '.join(level_topics)} in JSON array format with keys question, options, answer. Only return valid JSON array."

    # Generate questions using AI
    questions = ai_generate_branch_quiz(branch, prompt_text)

    if not questions:
        return jsonify({"success": False, "error": "Failed to generate branch quiz"}), 400

    return jsonify({
        "success": True,
        "branch": branch,
        "level": current_level,
        "topics": level_topics,
        "questions": questions,
        "student": {
            "uid_number": current_user['uid_number'],
            "name": current_user['name'],
            "email": current_user['email']
        }
    }), 200


# ----------------------------- Submit Branch Quiz -----------------------------
@app.route("/submit_branch_quiz", methods=["POST"])
@token_required
def submit_branch_quiz(current_user):
    try:
        data = request.get_json()

        score = data.get("score", 0)
        total = data.get("total", 10)
        branch = current_user.get("branch", "")
        uid_number = current_user.get("uid_number")

        if not branch:
            return jsonify({"success": False, "error": "Branch missing"}), 400

        # Get current level from DB or default to 1
        student = students_collection.find_one({"uid_number": uid_number})
        current_level = student.get("current_level", 1)

        # Check if passed
        passed = score >= 8

        # Update level if passed
        new_level = current_level + 1 if passed else current_level
        students_collection.update_one(
            {"uid_number": uid_number},
            {"$set": {"current_level": new_level}}
        )

        # Store quiz result
        branchquiz_collection.insert_one({
            "uid_number": uid_number,
            "branch": branch,
            "level": current_level,
            "score": score,
            "passed": passed,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return jsonify({
            "success": True,
            "message": "Quiz submitted successfully",
            "score": score,
            "passed": passed,
            "previous_level": current_level,
            "new_level": new_level
        }), 200

    except Exception as e:
        print("❌ Error submitting branch quiz:", e)
        return jsonify({"success": False, "error": str(e)}), 500

# Fetch Quiz History
# -----------------------------
@app.route('/quiz_history', methods=['GET'])
@token_required
def quiz_history(current_user):
    uid_number = current_user['uid_number']
    history = list(quiz_collection.find({"uid_number": uid_number}, {"_id": 0}))
    return jsonify({"success": True, "history": history}), 200

# -----------------------------
# Logout (client deletes JWT)
# -----------------------------
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful (client should delete JWT)"}), 200



def ai_generate_branch_quiz(branch: str, prompt_text: str = None):
    prompt = prompt_text or f"""
    Generate 10 multiple-choice questions for the {branch} branch in JSON array:
    [
      {{"question": "Q text", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "answer": "A"}}
    ]
    Only return valid JSON array. No markdown, no code fences, no extra text.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
        questions = json.loads(text)
        if isinstance(questions, dict):
            questions = [questions]
        elif not isinstance(questions, list):
            questions = []
        return questions
    except Exception as e:
        print("❌ Google AI branch quiz error:", e)
        return []



# Fetch student profile
@app.route("/get_student_profile", methods=["GET"])
@token_required
def get_student_profile(current_user):
    try:
        # Base student details
        profile = {
            "name": current_user.get("name", ""),
            "uid_number": current_user.get("uid_number", ""),
            "branch": current_user.get("branch", ""),
            "profile_image": current_user.get("profile_image", "")
        }

        uid_number = current_user.get("uid_number", "")

        # Count aptitude quiz attempts
        aptitude_attempts = quiz_results.count_documents({"uid_number": uid_number})

        # Fetch branch quiz progress
        branch_data = branchquiz.find_one({"uid_number": uid_number}, {"_id": 0, "current_level": 1})
        current_branch_level = branch_data.get("current_level", 0) if branch_data else 0

        # Combine all data
        profile["aptitude_attempted"] = aptitude_attempts
        profile["branch_level"] = current_branch_level

        return jsonify({"success": True, "profile": profile}), 200

    except Exception as e:
        print(f"Error fetching student profile: {e}")
        return jsonify({"success": False, "error": f"Failed to load profile: {str(e)}"}), 500



# Upload profile image
@app.route("/upload_profile_image", methods=["POST"])
@token_required
def upload_profile_image(current_user):
    data = request.get_json()
    if not data or 'image_base64' not in data:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    try:
        students_collection.update_one(
            {"uid_number": current_user['uid_number']},
            {"$set": {"profile_image": data['image_base64']}}
        )
        return jsonify({"success": True, "message": "Profile image uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    



    
# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
