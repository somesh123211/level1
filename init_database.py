#!/usr/bin/env python3
"""
Database Initialization Script
This script initializes the MongoDB database with sample data for testing
"""

import os
from dotenv import load_dotenv
from database_operations import QuizDatabase
from database_schema import DatabaseManager

# Load environment variables
load_dotenv()

def initialize_database():
    """Initialize the database with sample data"""
    
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("[ERROR] MONGO_URI not found in environment variables")
        return False
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager(MONGO_URI)
        quiz_db = QuizDatabase(MONGO_URI)
        
        print("[SUCCESS] Database manager initialized")
        
        # Create sample students
        sample_students = [
            {
                "email": "john.doe@example.com",
                "name": "John Doe",
                "branch": "Computer Science",
                "year": "2024"
            },
            {
                "email": "jane.smith@example.com", 
                "name": "Jane Smith",
                "branch": "Information Technology",
                "year": "2024"
            },
            {
                "email": "mike.wilson@example.com",
                "name": "Mike Wilson", 
                "branch": "Electronics",
                "year": "2023"
            }
        ]
        
        for student in sample_students:
            try:
                quiz_db.create_student(student)
                print(f"[SUCCESS] Created student: {student['name']}")
            except Exception as e:
                print(f"[WARNING] Student {student['name']} may already exist: {e}")
        
        # Create sample quizzes
        sample_quizzes = [
            {
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
            },
            {
                "quiz_id": "infosys_aptitude_basic_001",
                "company": "infosys",
                "type": "aptitude",
                "title": "Infosys Aptitude Test - Basic Level",
                "description": "Basic aptitude questions for Infosys placement preparation",
                "questions": [
                    {
                        "question_id": "q1",
                        "question": "If a train travels 120 km in 2 hours, what is its speed in m/s?",
                        "options": ["16.67 m/s", "60 m/s", "120 m/s", "240 m/s"],
                        "correct_answer": 0,
                        "explanation": "Speed = Distance/Time = 120km/2hr = 60 km/hr = 60*1000/3600 = 16.67 m/s",
                        "difficulty": 0.5,
                        "topic": "Mathematics",
                        "time_limit": 60,
                        "points": 1
                    },
                    {
                        "question_id": "q2",
                        "question": "Find the factorial of 5",
                        "options": ["120", "60", "24", "720"],
                        "correct_answer": 0,
                        "explanation": "5! = 5 × 4 × 3 × 2 × 1 = 120",
                        "difficulty": 0.6,
                        "topic": "Mathematics",
                        "time_limit": 45,
                        "points": 1
                    }
                ],
                "total_time_limit": 1200,  # 20 minutes
                "difficulty_level": "easy",
                "created_by": "admin"
            },
            {
                "quiz_id": "microsoft_coding_basic_001",
                "company": "microsoft",
                "type": "coding",
                "title": "Microsoft Coding Challenge - Basic Level",
                "description": "Basic coding questions for Microsoft placement preparation",
                "questions": [
                    {
                        "question_id": "q1",
                        "question": "Implement a function to reverse a string",
                        "options": ["Use built-in reverse()", "Use two pointers", "Use recursion", "All of the above"],
                        "correct_answer": 3,
                        "explanation": "All methods can be used to reverse a string",
                        "difficulty": 0.6,
                        "topic": "String Manipulation",
                        "time_limit": 300,
                        "points": 2
                    },
                    {
                        "question_id": "q2",
                        "question": "What is the time complexity of merge sort?",
                        "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
                        "correct_answer": 2,
                        "explanation": "Merge sort has O(n log n) time complexity in all cases",
                        "difficulty": 0.8,
                        "topic": "Algorithms",
                        "time_limit": 60,
                        "points": 1
                    }
                ],
                "total_time_limit": 2400,  # 40 minutes
                "difficulty_level": "hard",
                "created_by": "admin"
            }
        ]
        
        for quiz in sample_quizzes:
            try:
                quiz_db.create_quiz(quiz)
                print(f"[SUCCESS] Created quiz: {quiz['title']}")
            except Exception as e:
                print(f"[WARNING] Quiz {quiz['title']} may already exist: {e}")
        
        print("\n[SUCCESS] Database initialization completed!")
        print("\nSample data created:")
        print("- 3 sample students")
        print("- 3 sample quizzes (TCS, Infosys, Microsoft)")
        print("- Database indexes and collections")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        return False

def test_database_operations():
    """Test database operations with sample data"""
    
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        print("[ERROR] MONGO_URI not found in environment variables")
        return False
    
    try:
        quiz_db = QuizDatabase(MONGO_URI)
        
        # Test getting students
        students = [
            quiz_db.get_student("john.doe@example.com"),
            quiz_db.get_student("jane.smith@example.com"),
            quiz_db.get_student("mike.wilson@example.com")
        ]
        
        print("\n[TEST] Student data:")
        for student in students:
            if student:
                print(f"- {student['name']} ({student['email']}) - {student['branch']}")
        
        # Test getting quizzes
        quizzes = [
            quiz_db.get_quiz("tcs_aptitude_basic_001"),
            quiz_db.get_quiz("infosys_aptitude_basic_001"),
            quiz_db.get_quiz("microsoft_coding_basic_001")
        ]
        
        print("\n[TEST] Quiz data:")
        for quiz in quizzes:
            if quiz:
                print(f"- {quiz['title']} ({quiz['company']}) - {len(quiz['questions'])} questions")
        
        # Test starting a quiz attempt
        attempt_id = quiz_db.start_quiz_attempt(
            "john.doe@example.com", 
            "tcs_aptitude_basic_001",
            {"browser": "Chrome", "os": "Windows"}
        )
        
        print(f"\n[TEST] Started quiz attempt: {attempt_id}")
        
        # Test submitting answers
        quiz_db.submit_quiz_response(attempt_id, "q1", 2, 45)  # Correct answer
        quiz_db.submit_quiz_response(attempt_id, "q2", 3, 30)  # Correct answer
        quiz_db.submit_quiz_response(attempt_id, "q3", 1, 60)  # Correct answer
        
        # Complete the quiz
        quiz_db.complete_quiz_attempt(attempt_id, {"tab_switches": 0})
        
        print("[TEST] Quiz attempt completed successfully!")
        
        # Get performance data
        performance = quiz_db.get_student_performance("john.doe@example.com")
        print(f"\n[TEST] Performance data: {len(performance)} records")
        
        # Get leaderboard
        leaderboard = quiz_db.get_leaderboard(limit=10)
        print(f"[TEST] Leaderboard: {len(leaderboard)} entries")
        
        print("\n[SUCCESS] All database operations tested successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Database testing failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Initializing AI-Powered Placement Platform Database")
    print("=" * 60)
    
    # Initialize database
    if initialize_database():
        print("\n" + "=" * 60)
        print("🧪 Testing Database Operations")
        print("=" * 60)
        
        # Test operations
        if test_database_operations():
            print("\n🎉 Database setup and testing completed successfully!")
            print("\nYour database is ready with:")
            print("- Comprehensive quiz data storage")
            print("- Student performance tracking")
            print("- Analytics and reporting")
            print("- Leaderboard functionality")
        else:
            print("\n⚠️ Database testing failed, but initialization was successful")
    else:
        print("\n❌ Database initialization failed")
        return False
    
    return True

if __name__ == "__main__":
    main()
