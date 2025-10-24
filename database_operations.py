"""
Database Operations for Quiz Data Management
This module handles all database operations for storing and retrieving quiz data,
student responses, scores, and analytics.
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
import json
import uuid

class QuizDatabase:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["placement_platform"]
    
    # =============================================================================
    # STUDENT OPERATIONS
    # =============================================================================
    
    def create_student(self, student_data):
        """Create a new student record"""
        students = self.db["students"]
        student_data["created_at"] = datetime.now()
        student_data["last_login"] = datetime.now()
        student_data["total_quizzes_attempted"] = 0
        student_data["total_score"] = 0
        student_data["average_score"] = 0
        student_data["strong_topics"] = []
        student_data["weak_topics"] = []
        
        result = students.insert_one(student_data)
        return result.inserted_id
    
    def get_student(self, email):
        """Get student by email"""
        students = self.db["students"]
        return students.find_one({"email": email})
    
    def update_student_stats(self, email, quiz_score, questions_count):
        """Update student statistics after quiz completion"""
        students = self.db["students"]
        student = students.find_one({"email": email})
        
        if student:
            new_total_quizzes = student.get("total_quizzes_attempted", 0) + 1
            new_total_score = student.get("total_score", 0) + quiz_score
            new_average = new_total_score / new_total_quizzes if new_total_quizzes > 0 else 0
            
            students.update_one(
                {"email": email},
                {
                    "$set": {
                        "total_quizzes_attempted": new_total_quizzes,
                        "total_score": new_total_score,
                        "average_score": new_average,
                        "last_login": datetime.now()
                    }
                }
            )
    
    # =============================================================================
    # QUIZ OPERATIONS
    # =============================================================================
    
    def create_quiz(self, quiz_data):
        """Create a new quiz"""
        quizzes = self.db["quizzes"]
        quiz_data["created_at"] = datetime.now()
        quiz_data["is_active"] = True
        quiz_data["total_questions"] = len(quiz_data.get("questions", []))
        
        result = quizzes.insert_one(quiz_data)
        return result.inserted_id
    
    def get_quiz(self, quiz_id):
        """Get quiz by ID"""
        quizzes = self.db["quizzes"]
        return quizzes.find_one({"quiz_id": quiz_id})
    
    def get_quizzes_by_company(self, company, quiz_type="aptitude"):
        """Get quizzes by company and type"""
        quizzes = self.db["quizzes"]
        return list(quizzes.find({
            "company": company.lower(),
            "type": quiz_type,
            "is_active": True
        }))
    
    # =============================================================================
    # QUIZ ATTEMPT OPERATIONS
    # =============================================================================
    
    def start_quiz_attempt(self, student_email, quiz_id, device_info=None):
        """Start a new quiz attempt"""
        quiz_attempts = self.db["quiz_attempts"]
        
        attempt_data = {
            "attempt_id": str(uuid.uuid4()),
            "student_email": student_email,
            "quiz_id": quiz_id,
            "quiz": self.get_quiz(quiz_id),
            "started_at": datetime.now(),
            "completed_at": None,
            "time_taken": 0,
            "status": "in_progress",
            "score": 0,
            "max_score": 0,
            "percentage": 0,
            "questions_answered": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "skipped_questions": 0,
            "behavior_data": {
                "tab_switches": 0,
                "fullscreen_exits": 0,
                "copy_paste_attempts": 0,
                "right_clicks": 0,
                "suspicious_activities": []
            },
            "device_info": device_info or {},
            "responses": []
        }
        
        # Get quiz details
        quiz = self.get_quiz(quiz_id)
        if quiz:
            attempt_data["company"] = quiz.get("company")
            attempt_data["type"] = quiz.get("type")
            attempt_data["max_score"] = sum(q.get("points", 1) for q in quiz.get("questions", []))
        
        result = quiz_attempts.insert_one(attempt_data)
        return attempt_data["attempt_id"]
    
    def submit_quiz_response(self, attempt_id, question_id, selected_answer, response_time):
        """Submit a response for a specific question"""
        quiz_attempts = self.db["quiz_attempts"]
        student_responses = self.db["student_responses"]
        
        # Get attempt and quiz data
        attempt = quiz_attempts.find_one({"attempt_id": attempt_id})
        if not attempt:
            return False
        
        quiz = attempt.get("quiz", {})
        questions = quiz.get("questions", [])
        
        # Find the question
        question_data = None
        for q in questions:
            if q.get("question_id") == question_id:
                question_data = q
                break
        
        if not question_data:
            return False
        
        # Check if answer is correct
        correct_answer = question_data.get("correct_answer")
        is_correct = selected_answer == correct_answer
        points_earned = question_data.get("points", 1) if is_correct else 0
        
        # Store individual response
        response_data = {
            "attempt_id": attempt_id,
            "student_email": attempt["student_email"],
            "question_id": question_id,
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "response_time": response_time,
            "time_spent": response_time,
            "points_earned": points_earned,
            "answered_at": datetime.now(),
            "question_data": {
                "question": question_data.get("question"),
                "options": question_data.get("options"),
                "difficulty": question_data.get("difficulty"),
                "topic": question_data.get("topic")
            }
        }
        
        student_responses.insert_one(response_data)
        
        # Update attempt data
        new_score = attempt["score"] + points_earned
        new_questions_answered = attempt["questions_answered"] + 1
        new_correct_answers = attempt["correct_answers"] + (1 if is_correct else 0)
        new_incorrect_answers = attempt["incorrect_answers"] + (1 if not is_correct else 0)
        
        quiz_attempts.update_one(
            {"attempt_id": attempt_id},
            {
                "$set": {
                    "score": new_score,
                    "questions_answered": new_questions_answered,
                    "correct_answers": new_correct_answers,
                    "incorrect_answers": new_incorrect_answers,
                    "percentage": (new_score / attempt["max_score"]) * 100 if attempt["max_score"] > 0 else 0
                },
                "$push": {"responses": response_data}
            }
        )
        
        return True
    
    def complete_quiz_attempt(self, attempt_id, behavior_data=None):
        """Complete a quiz attempt and calculate final results"""
        quiz_attempts = self.db["quiz_attempts"]
        
        attempt = quiz_attempts.find_one({"attempt_id": attempt_id})
        if not attempt:
            return False
        
        # Calculate time taken
        time_taken = (datetime.now() - attempt["started_at"]).total_seconds()
        
        # Update attempt with completion data
        update_data = {
            "completed_at": datetime.now(),
            "time_taken": time_taken,
            "status": "completed"
        }
        
        if behavior_data:
            update_data["behavior_data"] = behavior_data
        
        quiz_attempts.update_one(
            {"attempt_id": attempt_id},
            {"$set": update_data}
        )
        
        # Update student statistics
        self.update_student_stats(
            attempt["student_email"],
            attempt["score"],
            attempt["questions_answered"]
        )
        
        # Update performance analytics
        self.update_performance_analytics(attempt)
        
        return True
    
    # =============================================================================
    # ANALYTICS OPERATIONS
    # =============================================================================
    
    def update_performance_analytics(self, attempt):
        """Update performance analytics for a student"""
        performance_analytics = self.db["performance_analytics"]
        
        student_email = attempt["student_email"]
        company = attempt["company"]
        
        # Get existing analytics or create new
        existing = performance_analytics.find_one({
            "student_email": student_email,
            "company": company
        })
        
        if existing:
            # Update existing analytics
            new_total_attempts = existing["total_attempts"] + 1
            new_total_questions = existing["total_questions"] + attempt["questions_answered"]
            new_correct_answers = existing["correct_answers"] + attempt["correct_answers"]
            new_total_score = existing["total_score"] + attempt["score"]
            
            performance_analytics.update_one(
                {"student_email": student_email, "company": company},
                {
                    "$set": {
                        "total_attempts": new_total_attempts,
                        "total_questions": new_total_questions,
                        "correct_answers": new_correct_answers,
                        "total_score": new_total_score,
                        "average_score": (new_total_score / new_total_questions) * 100 if new_total_questions > 0 else 0,
                        "calculated_at": datetime.now()
                    }
                }
            )
        else:
            # Create new analytics record
            analytics_data = {
                "student_email": student_email,
                "company": company,
                "total_attempts": 1,
                "total_questions": attempt["questions_answered"],
                "correct_answers": attempt["correct_answers"],
                "incorrect_answers": attempt["incorrect_answers"],
                "skipped_questions": attempt["skipped_questions"],
                "total_score": attempt["score"],
                "max_possible_score": attempt["max_score"],
                "average_score": attempt["percentage"],
                "average_response_time": attempt["time_taken"] / attempt["questions_answered"] if attempt["questions_answered"] > 0 else 0,
                "improvement_trend": "stable",
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "calculated_at": datetime.now()
            }
            
            performance_analytics.insert_one(analytics_data)
    
    def get_student_performance(self, student_email, company=None):
        """Get comprehensive performance data for a student"""
        performance_analytics = self.db["performance_analytics"]
        
        query = {"student_email": student_email}
        if company:
            query["company"] = company
        
        return list(performance_analytics.find(query).sort("calculated_at", DESCENDING))
    
    def get_quiz_statistics(self, quiz_id):
        """Get statistics for a specific quiz"""
        quiz_attempts = self.db["quiz_attempts"]
        
        attempts = list(quiz_attempts.find({"quiz_id": quiz_id, "status": "completed"}))
        
        if not attempts:
            return None
        
        total_attempts = len(attempts)
        total_students = len(set(attempt["student_email"] for attempt in attempts))
        scores = [attempt["percentage"] for attempt in attempts]
        times = [attempt["time_taken"] for attempt in attempts]
        
        statistics = {
            "quiz_id": quiz_id,
            "total_attempts": total_attempts,
            "total_students": total_students,
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "completion_rate": 100.0,  # All completed attempts
            "average_time_taken": sum(times) / len(times),
            "calculated_at": datetime.now()
        }
        
        return statistics
    
    def get_leaderboard(self, company=None, limit=50):
        """Get leaderboard data"""
        performance_analytics = self.db["performance_analytics"]
        
        query = {}
        if company:
            query["company"] = company
        
        # Aggregate to get best scores per student
        pipeline = [
            {"$match": query},
            {"$sort": {"average_score": DESCENDING}},
            {"$limit": limit},
            {
                "$lookup": {
                    "from": "students",
                    "localField": "student_email",
                    "foreignField": "email",
                    "as": "student_info"
                }
            },
            {
                "$project": {
                    "student_email": 1,
                    "student_name": {"$arrayElemAt": ["$student_info.name", 0]},
                    "branch": {"$arrayElemAt": ["$student_info.branch", 0]},
                    "company": 1,
                    "average_score": 1,
                    "total_attempts": 1,
                    "total_questions": 1,
                    "correct_answers": 1
                }
            }
        ]
        
        return list(performance_analytics.aggregate(pipeline))
    
    # =============================================================================
    # REPORTING OPERATIONS
    # =============================================================================
    
    def get_student_quiz_history(self, student_email, limit=20):
        """Get quiz attempt history for a student"""
        quiz_attempts = self.db["quiz_attempts"]
        
        return list(quiz_attempts.find(
            {"student_email": student_email}
        ).sort("started_at", DESCENDING).limit(limit))
    
    def get_detailed_quiz_results(self, attempt_id):
        """Get detailed results for a specific quiz attempt"""
        quiz_attempts = self.db["quiz_attempts"]
        student_responses = self.db["student_responses"]
        
        attempt = quiz_attempts.find_one({"attempt_id": attempt_id})
        if not attempt:
            return None
        
        responses = list(student_responses.find({"attempt_id": attempt_id}))
        
        return {
            "attempt": attempt,
            "responses": responses,
            "quiz_details": attempt.get("quiz", {})
        }
    
    def get_company_performance_summary(self, company):
        """Get performance summary for a company"""
        performance_analytics = self.db["performance_analytics"]
        quiz_attempts = self.db["quiz_attempts"]
        
        # Get analytics data
        analytics = list(performance_analytics.find({"company": company}))
        
        # Get attempt data
        attempts = list(quiz_attempts.find({"company": company, "status": "completed"}))
        
        if not analytics:
            return None
        
        summary = {
            "company": company,
            "total_students": len(set(a["student_email"] for a in analytics)),
            "total_attempts": sum(a["total_attempts"] for a in analytics),
            "total_questions": sum(a["total_questions"] for a in analytics),
            "average_score": sum(a["average_score"] for a in analytics) / len(analytics),
            "completion_rate": len(attempts) / max(len(set(a["student_email"] for a in attempts)), 1) * 100,
            "generated_at": datetime.now()
        }
        
        return summary

# Example usage functions
def create_sample_quiz_data(db):
    """Create sample quiz data for testing"""
    
    # Sample TCS Aptitude Quiz
    tcs_quiz = {
        "quiz_id": "tcs_aptitude_basic_001",
        "company": "tcs",
        "type": "aptitude",
        "title": "TCS Aptitude Test - Basic Level",
        "description": "Basic aptitude questions for TCS placement preparation",
        "questions": [
            {
                "question_id": "q1",
                "question": "What is the output of: int x = 5; System.out.println(x++ + ++x);",
                "options": ["10", "11", "12", "13"],
                "correct_answer": 2,
                "explanation": "x++ returns 5 then increments to 6, ++x increments to 7 then returns 7, so 5+7=12",
                "difficulty": 0.7,
                "topic": "Java Basics",
                "time_limit": 60,
                "points": 1
            },
            {
                "question_id": "q2",
                "question": "Which of the following is not a valid Java keyword?",
                "options": ["abstract", "assert", "boolean", "main"],
                "correct_answer": 3,
                "explanation": "main is not a keyword, it's a method name",
                "difficulty": 0.5,
                "topic": "Java Basics",
                "time_limit": 45,
                "points": 1
            },
            {
                "question_id": "q3",
                "question": "What is the time complexity of binary search?",
                "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                "correct_answer": 1,
                "explanation": "Binary search has O(log n) time complexity",
                "difficulty": 0.8,
                "topic": "Algorithms",
                "time_limit": 60,
                "points": 1
            }
        ],
        "total_time_limit": 1800,  # 30 minutes
        "difficulty_level": "medium",
        "created_by": "admin"
    }
    
    db.create_quiz(tcs_quiz)
    print("✅ Sample TCS quiz created!")

if __name__ == "__main__":
    # Test the database operations
    MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
    db = QuizDatabase(MONGO_URI)
    
    # Create sample data
    create_sample_quiz_data(db)
    
    print("Database operations test completed!")
