#!/usr/bin/env python3
"""
Setup script for AI-Powered Placement Platform
This script helps set up the environment and install dependencies
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ['certificates', 'logs', 'uploads', 'temp']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Error creating directory {directory}: {e}")
            return False
    
    return True

def check_environment():
    """Check if environment file exists"""
    print("🔍 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print("📝 Please copy env_example.txt to .env and configure your settings:")
        print("   - MongoDB URI")
        print("   - SendGrid API credentials")
        print("   - OpenAI API key")
        print("   - Secret key for Flask")
        return False
    else:
        print("✅ Environment file found!")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI-Powered Placement Platform...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Download NLTK data
    if not download_nltk_data():
        print("⚠️  NLTK data download failed, but continuing...")
    
    # Create directories
    if not create_directories():
        print("❌ Setup failed at directory creation")
        return False
    
    # Check environment
    env_ok = check_environment()
    
    print("=" * 50)
    if env_ok:
        print("🎉 Setup completed successfully!")
        print("📖 Please read README_AI_FEATURES.md for detailed usage instructions")
        print("🚀 Run the application with: python app.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("📝 Please configure your .env file before running the application")
    
    return True

if __name__ == "__main__":
    main()
