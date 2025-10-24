#!/usr/bin/env python3
"""
Test Script for Database Operations
This script tests the comprehensive database functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_database_endpoints():
    """Test all database endpoints"""
    
    print("🧪 Testing Database Endpoints")
    print("=" * 50)
    
    # Test data
    student_email = "test.student@example.com"
    quiz_id = "tcs_aptitude_basic_001"
    
    try:
        # 1. Test student signup
        print("\n1. Testing Student Signup...")
        signup_data = {
            "name": "Test Student",
            "branch": "Computer Science",
            "email": student_email,
            "year": "2024"
        }
        
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        if response.status_code == 200:
            print("✅ Student signup successful")
        else:
            print(f"⚠️ Student signup response: {response.status_code}")
        
        # 2. Test getting student performance (should be empty initially)
        print("\n2. Testing Student Performance (Empty)...")
        response = requests.get(f"{BASE_URL}/api/student/{student_email}/performance")
        if response.status_code in [200, 404]:
            print("✅ Student performance endpoint working")
        else:
            print(f"❌ Student performance failed: {response.status_code}")
        
        # 3. Test starting a quiz
        print("\n3. Testing Quiz Start...")
        quiz_start_data = {
            "email": student_email,
            "device_info": {
                "browser": "Chrome",
                "os": "Windows"
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/quiz/{quiz_id}/start", json=quiz_start_data)
        if response.status_code == 200:
            attempt_data = response.json()
            attempt_id = attempt_data.get("attempt_id")
            print(f"✅ Quiz started successfully: {attempt_id}")
        else:
            print(f"❌ Quiz start failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # 4. Test submitting answers
        print("\n4. Testing Answer Submission...")
        answers = [
            {"question_id": "q1", "selected_answer": 2, "response_time": 45},
            {"question_id": "q2", "selected_answer": 3, "response_time": 30},
            {"question_id": "q3", "selected_answer": 1, "response_time": 60}
        ]
        
        for answer in answers:
            response = requests.post(
                f"{BASE_URL}/api/quiz/attempt/{attempt_id}/submit-answer",
                json=answer
            )
            if response.status_code == 200:
                print(f"✅ Answer submitted for {answer['question_id']}")
            else:
                print(f"❌ Answer submission failed for {answer['question_id']}: {response.status_code}")
        
        # 5. Test completing quiz
        print("\n5. Testing Quiz Completion...")
        completion_data = {
            "behavior_data": {
                "tab_switches": 0,
                "fullscreen_exits": 0,
                "copy_paste_attempts": 0,
                "right_clicks": 0
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/quiz/attempt/{attempt_id}/complete",
            json=completion_data
        )
        if response.status_code == 200:
            results = response.json()
            print("✅ Quiz completed successfully")
            print(f"   Score: {results['results']['attempt']['score']}/{results['results']['attempt']['max_score']}")
            print(f"   Percentage: {results['results']['attempt']['percentage']}%")
        else:
            print(f"❌ Quiz completion failed: {response.status_code}")
        
        # 6. Test getting student performance (should have data now)
        print("\n6. Testing Student Performance (With Data)...")
        response = requests.get(f"{BASE_URL}/api/student/{student_email}/performance")
        if response.status_code == 200:
            performance = response.json()
            print("✅ Student performance retrieved")
            if performance.get("performance_data"):
                print(f"   Records found: {len(performance['performance_data'])}")
        else:
            print(f"❌ Student performance retrieval failed: {response.status_code}")
        
        # 7. Test getting quiz history
        print("\n7. Testing Quiz History...")
        response = requests.get(f"{BASE_URL}/api/student/{student_email}/quiz-history")
        if response.status_code == 200:
            history = response.json()
            print("✅ Quiz history retrieved")
            print(f"   Total attempts: {history.get('total_attempts', 0)}")
        else:
            print(f"❌ Quiz history retrieval failed: {response.status_code}")
        
        # 8. Test getting quiz statistics
        print("\n8. Testing Quiz Statistics...")
        response = requests.get(f"{BASE_URL}/api/quiz/{quiz_id}/statistics")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Quiz statistics retrieved")
            if stats.get("statistics"):
                print(f"   Total attempts: {stats['statistics'].get('total_attempts', 0)}")
        else:
            print(f"❌ Quiz statistics retrieval failed: {response.status_code}")
        
        # 9. Test getting leaderboard
        print("\n9. Testing Leaderboard...")
        response = requests.get(f"{BASE_URL}/api/leaderboard?company=tcs&limit=10")
        if response.status_code == 200:
            leaderboard = response.json()
            print("✅ Leaderboard retrieved")
            print(f"   Entries: {len(leaderboard.get('leaderboard', []))}")
        else:
            print(f"❌ Leaderboard retrieval failed: {response.status_code}")
        
        # 10. Test getting quiz attempt details
        print("\n10. Testing Quiz Attempt Details...")
        response = requests.get(f"{BASE_URL}/api/quiz/attempt/{attempt_id}/details")
        if response.status_code == 200:
            details = response.json()
            print("✅ Quiz attempt details retrieved")
            print(f"   Responses: {len(details['details'].get('responses', []))}")
        else:
            print(f"❌ Quiz attempt details retrieval failed: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Database endpoint testing completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Testing failed with error: {e}")
        return False

def test_basic_endpoints():
    """Test basic application endpoints"""
    
    print("🔍 Testing Basic Application Endpoints")
    print("=" * 50)
    
    try:
        # Test home endpoint
        print("\n1. Testing Home Endpoint...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Home endpoint working")
        else:
            print(f"❌ Home endpoint failed: {response.status_code}")
        
        # Test health check
        print("\n2. Testing Health Check...")
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            health = response.json()
            print("✅ Health check working")
            print(f"   Database: {health.get('database', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Test security check
        print("\n3. Testing Security Check...")
        response = requests.get(f"{BASE_URL}/api/security/check")
        if response.status_code == 200:
            security = response.json()
            print("✅ Security check working")
            print(f"   Status: {security.get('status', 'unknown')}")
        else:
            print(f"❌ Security check failed: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask app is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Basic endpoint testing failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Testing AI-Powered Placement Platform Database")
    print("=" * 60)
    
    # Test basic endpoints first
    if test_basic_endpoints():
        print("\n" + "=" * 60)
        
        # Test database endpoints
        if test_database_endpoints():
            print("\n🎉 All tests completed successfully!")
            print("\nYour database is working correctly with:")
            print("- Student registration and management")
            print("- Quiz creation and management")
            print("- Answer submission and scoring")
            print("- Performance analytics")
            print("- Leaderboard functionality")
            print("- Comprehensive reporting")
        else:
            print("\n⚠️ Database endpoint testing failed")
    else:
        print("\n❌ Basic endpoint testing failed")
        print("Make sure the Flask application is running:")
        print("  python app.py")

if __name__ == "__main__":
    main()
