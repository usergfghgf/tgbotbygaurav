#!/usr/bin/env python3
"""
Streamlit Dashboard for Telegram Bot
This provides a dashboard to monitor and manage your bot
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_configuration():
    """Check if all required configuration is present"""
    bot_token = os.getenv('BOT_TOKEN')
    cerebras_api_key = os.getenv('CEREBRAS_API_KEY')
    
    if not bot_token:
        st.error("❌ BOT_TOKEN not configured!")
        st.info("Please set BOT_TOKEN in your environment variables")
        return False
    
    if not cerebras_api_key:
        st.error("❌ CEREBRAS_API_KEY not configured!")
        st.info("Please set CEREBRAS_API_KEY in your environment variables")
        return False
    
    return True

def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="Telegram Bot Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Telegram Bot Dashboard")
    st.markdown("---")
    
    # Check configuration
    if not check_configuration():
        st.stop()
    
    # Sidebar for controls
    st.sidebar.header("Bot Controls")
    
    # Display configuration status
    st.sidebar.subheader("Configuration Status")
    bot_token = os.getenv('BOT_TOKEN')
    cerebras_api_key = os.getenv('CEREBRAS_API_KEY')
    bot_owner_id = os.getenv('BOT_OWNER_ID')
    
    st.sidebar.success("✅ BOT_TOKEN configured")
    st.sidebar.success("✅ CEREBRAS_API_KEY configured")
    
    if bot_owner_id:
        st.sidebar.success("✅ BOT_OWNER_ID configured")
    else:
        st.sidebar.warning("⚠️ BOT_OWNER_ID not configured")
    
    # Main content area
    st.success("🎉 Configuration verified successfully!")
    
    # Bot information
    st.subheader("Bot Information")
    
    try:
        from config import ROLES
        st.write(f"**Available Roles:** {len(ROLES)}")
        
        # Display roles
        roles_data = []
        for role_key, role_info in ROLES.items():
            roles_data.append({
                "Role": role_info['name'],
                "Description": role_info['description'],
                "Key": role_key
            })
        
        st.dataframe(roles_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading bot information: {e}")
    
    # Bot commands
    st.subheader("Available Commands")
    commands = [
        "/start - Start the bot",
        "/roles - Choose AI companion role",
        "/help - Show help",
        "/clear - Clear conversation",
        "/status - Show current status",
        "/ping - Check response time",
        "/currentmodel - Show current AI model"
    ]
    
    for cmd in commands:
        st.write(f"• {cmd}")
    
    # Owner commands
    if bot_owner_id:
        st.subheader("Owner Commands")
        owner_commands = [
            "/models - Show available models",
            "/setmodel <name> - Set AI model",
            "/debug - Show debug info"
        ]
        for cmd in owner_commands:
            st.write(f"• {cmd}")
    
    # Deployment Instructions
    st.subheader("🚀 How to Run Your Bot")
    
    st.markdown("""
    ### Option 1: Run Locally (Recommended)
    
    Since Streamlit has limitations with long-running processes, run your bot locally:
    
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    
    # Run the bot
    python simple_bot.py
    ```
    
    ### Option 2: Deploy on Railway/Render/Heroku
    
    1. **Upload your code to GitHub**
    2. **Connect to Railway/Render/Heroku**
    3. **Set environment variables:**
       - `BOT_TOKEN` = Your Telegram bot token
       - `CEREBRAS_API_KEY` = Your Cerebras API key
       - `BOT_OWNER_ID` = Your Telegram user ID (optional)
    4. **Deploy!**
    
    ### Option 3: Use Python Anywhere
    
    1. Upload your files to Python Anywhere
    2. Set up environment variables
    3. Run `python simple_bot.py` in a console
    4. Keep the console running
    
    ### Option 4: VPS/Server
    
    1. Upload your code to a VPS
    2. Install Python and dependencies
    3. Run with `nohup python simple_bot.py &`
    4. Bot will run in background
    """)
    
    # Bot features
    st.subheader("Bot Features")
    st.markdown("""
    - **Multiple AI Personalities:** Choose from 7 different roles
    - **Role-based Responses:** Each role has unique personality and expertise
    - **Conversation Memory:** Bot remembers chat history (last 20 messages)
    - **Model Management:** Switch between different AI models
    - **Partner Roles:** Create personalized boyfriend/girlfriend companions
    - **Real-time Status Monitoring**
    """)
    
    # Troubleshooting
    st.subheader("🔧 Troubleshooting")
    
    st.markdown("""
    ### Common Issues:
    
    1. **Bot not responding:**
       - Check if bot is running: `python simple_bot.py`
       - Verify environment variables are set
       - Check bot token is valid
    
    2. **API errors:**
       - Verify Cerebras API key is valid
       - Check internet connection
       - Ensure API quota is available
    
    3. **Import errors:**
       - Install dependencies: `pip install -r requirements.txt`
       - Check Python version (3.8+)
    
    4. **Streamlit limitations:**
       - Streamlit is for dashboards, not long-running bots
       - Use local deployment or cloud platforms
    """)
    
    # Quick Test
    st.subheader("🧪 Quick Test")
    
    if st.button("Test Bot Configuration"):
        try:
            from config import BOT_TOKEN, CEREBRAS_API_KEY, ROLES
            from cerebras_client import CerebrasClient
            from user_manager import UserManager
            
            st.success("✅ All imports successful!")
            st.success("✅ Configuration loaded!")
            st.success("✅ Bot components ready!")
            
            # Test API connection
            client = CerebrasClient()
            if client.is_api_key_valid():
                st.success("✅ Cerebras API key is valid!")
            else:
                st.error("❌ Cerebras API key is invalid!")
                
        except Exception as e:
            st.error(f"❌ Configuration test failed: {e}")

if __name__ == "__main__":
    main()
