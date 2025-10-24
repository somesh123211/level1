import requests

BASE_URL = "http://127.0.0.1:5000"

# -----------------------------
# User A session
# -----------------------------
session_a = requests.Session()
login_a = session_a.post(f"{BASE_URL}/login", json={"email": "userA@example.com", "password": "passwordA"})
print("User A login:", login_a.json())

quiz_a = session_a.get(f"{BASE_URL}/start_quiz/Aptitude")
print("User A quiz:", quiz_a.json()["questions"][0:3])  # print first 3 questions

# -----------------------------
# User B session
# -----------------------------
session_b = requests.Session()
login_b = session_b.post(f"{BASE_URL}/login", json={"email": "userB@example.com", "password": "passwordB"})
print("User B login:", login_b.json())

quiz_b = session_b.get(f"{BASE_URL}/start_quiz/Aptitude")
print("User B quiz:", quiz_b.json()["questions"][0:3])
