# backend_flask/quiz_ai.py
import json
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY not set in .env")

# -----------------------------
# Configure Google AI (Gemini)
# -----------------------------
genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------
# Generate Questions
# -----------------------------
def generate_questions(quiz_type: str):
    """
    Generate 10 MCQs using Gemini 2.5 Flash.
    Returns a list of questions with keys: question, options, answer.
    """
    prompt = f"""
    Generate 10 {quiz_type} multiple-choice questions in JSON array:
    [
      {{
        "question": "Q text",
        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "answer": "A"
      }}
    ]
    Only return valid JSON array. No markdown, no code fences, no extra text.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean up accidental markdown or code fences
        text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.MULTILINE).strip()

        # Convert JSON string to Python list
        questions = json.loads(text)

        # Ensure questions is always a list
        if isinstance(questions, dict):
            questions = [questions]
        elif not isinstance(questions, list):
            questions = []

        # Optional: ensure each question has all required keys
        valid_questions = []
        for q in questions:
            if all(k in q for k in ["question", "options", "answer"]):
                valid_questions.append(q)

        return valid_questions

    except Exception as e:
        print("❌ Google AI API error:", e)
        return []

# -----------------------------
# Test run
# -----------------------------
if __name__ == "__main__":
    qs = generate_questions("aptitude")
    for i, q in enumerate(qs, start=1):
        print(f"Q{i}: {q['question']}")
        print("Options:", q['options'])
        print("Answer:", q['answer'])
        print("-" * 50)
