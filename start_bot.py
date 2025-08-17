#!/usr/bin/env python3
"""
Simple startup script for the Telegram bot
"""

import sys
import os
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    bot_token = os.getenv('BOT_TOKEN')
    cerebras_api_key = os.getenv('CEREBRAS_API_KEY')
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in .env file!")
        print("Please create a .env file with your BOT_TOKEN")
        return False
    
    if not cerebras_api_key:
        print("❌ CEREBRAS_API_KEY not found in .env file!")
        print("Please add your CEREBRAS_API_KEY to the .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main startup function"""
    print("🤖 Telegram Bot Startup")
    print("=" * 30)
    
    # Check environment
    if not check_environment():
        print("\n📝 Setup Instructions:")
        print("1. Copy env_example.txt to .env")
        print("2. Edit .env with your actual credentials")
        print("3. Run this script again")
        return
    
    # Test imports
    try:
        print("🔧 Testing imports...")
        from bot import main as bot_main
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return
    
    # Start the bot
    print("\n🚀 Starting bot...")
    try:
        bot_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")

if __name__ == "__main__":
    main()
