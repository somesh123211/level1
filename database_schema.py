"""
MongoDB Database Schema for AI-Powered Placement Platform
This file defines the complete database structure for storing quiz data, 
student responses, scores, and analytics.
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["placement_platform"]
        self.initialize_collections()
    
    def initialize_collections(self):
        """Initialize all collections with proper indexes"""
        
        # 1. STUDENTS COLLECTION
        students = self.db["students"]
        students.create_index("email", unique=True)
        students.create_index("branch")
        students.create_index("year")
        
        # 2. QUIZZES COLLECTION
        quizzes = self.db["quizzes"]
        quizzes.create_index([("company", ASCENDING), ("type", ASCENDING)])
        quizzes.create_index("difficulty")
        quizzes.create_index("topic")
        quizzes.create_index("created_at", DESCENDING)
        
        # 3. QUIZ_ATTEMPTS COLLECTION (Main collection for storing quiz attempts)
        quiz_attempts = self.db["quiz_attempts"]
        quiz_attempts.create_index("student_email")
        quiz_attempts.create_index("quiz_id")
        quiz_attempts.create_index([("student_email", ASCENDING), ("attempted_at", DESCENDING)])
        quiz_attempts.create_index("company")
        quiz_attempts.create_index("score")
        quiz_attempts.create_index("status")  # completed, in_progress, abandoned
        
        # 4. STUDENT_RESPONSES COLLECTION (Individual question responses)
        student_responses = self.db["student_responses"]
        student_responses.create_index("attempt_id")
        student_responses.create_index("student_email")
        student_responses.create_index("question_id")
        student_responses.create_index("is_correct")
        student_responses.create_index("response_time")
        
        # 5. PERFORMANCE_ANALYTICS COLLECTION
        performance_analytics = self.db["performance_analytics"]
        performance_analytics.create_index("student_email")
        performance_analytics.create_index("company")
        performance_analytics.create_index("topic")
        performance_analytics.create_index("calculated_at", DESCENDING)
        
        # 6. QUIZ_STATISTICS COLLECTION
        quiz_statistics = self.db["quiz_statistics"]
        quiz_statistics.create_index("quiz_id")
        quiz_statistics.create_index("company")
        quiz_statistics.create_index("topic")
        quiz_statistics.create_index("calculated_at", DESCENDING)
        
        # 7. STUDENT_PROGRESS COLLECTION
        student_progress = self.db["student_progress"]
        student_progress.create_index("student_email")
        student_progress.create_index("company")
        student_progress.create_index("topic")
        student_progress.create_index("updated_at", DESCENDING)
        
        # 8. LEADERBOARD COLLECTION
        leaderboard = self.db["leaderboard"]
        leaderboard.create_index("company")
        leaderboard.create_index("topic")
        leaderboard.create_index("time_period")
        leaderboard.create_index("calculated_at", DESCENDING)
        
        print("✅ Database collections and indexes created successfully!")

# Sample data structures for reference
SAMPLE_STUDENT = {
    "_id": None,  # Auto-generated
    "email": "student@example.com",
    "name": "John Doe",
    "branch": "Computer Science",
    "year": "2024",
    "created_at": datetime.now(),
    "last_login": datetime.now(),
    "total_quizzes_attempted": 0,
    "total_score": 0,
    "average_score": 0,
    "strong_topics": [],
    "weak_topics": []
}

SAMPLE_QUIZ = {
    "_id": None,  # Auto-generated
    "quiz_id": "tcs_aptitude_001",
    "company": "tcs",
    "type": "aptitude",  # aptitude, coding, technical
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
            "time_limit": 60,  # seconds
            "points": 1
        }
    ],
    "total_questions": 1,
    "total_time_limit": 3600,  # 1 hour
    "total_points": 1,
    "difficulty_level": "medium",
    "created_at": datetime.now(),
    "created_by": "admin",
    "is_active": True
}

SAMPLE_QUIZ_ATTEMPT = {
    "_id": None,  # Auto-generated
    "attempt_id": "attempt_123456789",
    "student_email": "student@example.com",
    "quiz_id": "tcs_aptitude_001",
    "company": "tcs",
    "type": "aptitude",
    "started_at": datetime.now(),
    "completed_at": None,
    "time_taken": 0,  # in seconds
    "status": "in_progress",  # in_progress, completed, abandoned, timed_out
    "score": 0,
    "max_score": 1,
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
    "device_info": {
        "browser": "Chrome",
        "os": "Windows",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0..."
    }
}

SAMPLE_STUDENT_RESPONSE = {
    "_id": None,  # Auto-generated
    "attempt_id": "attempt_123456789",
    "student_email": "student@example.com",
    "question_id": "q1",
    "selected_answer": 2,
    "correct_answer": 2,
    "is_correct": True,
    "response_time": 45,  # seconds taken to answer
    "time_spent": 45,
    "points_earned": 1,
    "answered_at": datetime.now(),
    "question_data": {
        "question": "What is the output of: int x = 5; System.out.println(x++ + ++x);",
        "options": ["10", "11", "12", "13"],
        "difficulty": 0.7,
        "topic": "Java Basics"
    }
}

SAMPLE_PERFORMANCE_ANALYTICS = {
    "_id": None,  # Auto-generated
    "student_email": "student@example.com",
    "company": "tcs",
    "topic": "Java Basics",
    "total_attempts": 5,
    "total_questions": 25,
    "correct_answers": 20,
    "incorrect_answers": 5,
    "skipped_questions": 0,
    "total_score": 20,
    "max_possible_score": 25,
    "average_score": 80.0,
    "average_response_time": 45.5,
    "improvement_trend": "improving",  # improving, declining, stable
    "strengths": ["Java Basics", "Data Structures"],
    "weaknesses": ["Algorithms", "Time Management"],
    "recommendations": [
        "Focus more on algorithm problems",
        "Practice time management techniques"
    ],
    "calculated_at": datetime.now()
}

SAMPLE_QUIZ_STATISTICS = {
    "_id": None,  # Auto-generated
    "quiz_id": "tcs_aptitude_001",
    "company": "tcs",
    "topic": "Java Basics",
    "total_attempts": 150,
    "total_students": 120,
    "average_score": 72.5,
    "highest_score": 95.0,
    "lowest_score": 25.0,
    "completion_rate": 85.0,  # percentage of students who completed
    "average_time_taken": 2800,  # seconds
    "difficulty_rating": 0.7,  # calculated based on performance
    "question_analytics": [
        {
            "question_id": "q1",
            "total_attempts": 150,
            "correct_attempts": 120,
            "accuracy_rate": 80.0,
            "average_time": 45.0,
            "difficulty_level": 0.7
        }
    ],
    "calculated_at": datetime.now()
}

SAMPLE_STUDENT_PROGRESS = {
    "_id": None,  # Auto-generated
    "student_email": "student@example.com",
    "overall_progress": {
        "total_quizzes_attempted": 15,
        "total_questions_answered": 150,
        "overall_average_score": 78.5,
        "improvement_rate": 12.5,  # percentage improvement over time
        "current_level": "intermediate"
    },
    "company_progress": {
        "tcs": {
            "attempts": 5,
            "average_score": 82.0,
            "last_attempt": datetime.now(),
            "improvement": "improving"
        },
        "infosys": {
            "attempts": 3,
            "average_score": 75.0,
            "last_attempt": datetime.now(),
            "improvement": "stable"
        }
    },
    "topic_progress": {
        "Java Basics": {
            "attempts": 8,
            "average_score": 85.0,
            "mastery_level": "expert"
        },
        "Data Structures": {
            "attempts": 5,
            "average_score": 70.0,
            "mastery_level": "intermediate"
        }
    },
    "updated_at": datetime.now()
}

def create_sample_data(db_manager):
    """Create sample data for testing"""
    
    # Insert sample student
    students = db_manager.db["students"]
    students.insert_one(SAMPLE_STUDENT.copy())
    
    # Insert sample quiz
    quizzes = db_manager.db["quizzes"]
    quizzes.insert_one(SAMPLE_QUIZ.copy())
    
    print("✅ Sample data created successfully!")

if __name__ == "__main__":
    # Initialize database
    MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
    db_manager = DatabaseManager(MONGO_URI)
    
    # Create sample data (optional)
    # create_sample_data(db_manager)
    
    print("Database setup completed!")
