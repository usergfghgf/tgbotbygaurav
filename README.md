# 🤖 Role-Based Telegram Chatbot

A sophisticated Telegram chatbot that adapts its personality and expertise based on user-selected roles. Built with Python and powered by the Cerebras AI API.

## ✨ Features

### 🎭 Multiple AI Personalities
- **Default Assistant** - General help and conversation
- **Code Expert** - Programming assistance and debugging
- **Data Analyst** - Data insights and statistical guidance
- **Male/Female Partner** - Supportive companion conversations
- **Supportive Friend** - Encouraging and uplifting interactions
- **Therapeutic Support** - Emotional guidance and coping strategies

### 🔧 Bot Commands
- `/start` - Initialize the bot and see welcome message
- `/roles` - Choose your AI companion's role
- `/help` - Display help information
- `/clear` - Clear conversation history
- `/status` - Show current role and status
- `/ping` - Check bot response time
- `/currentmodel` - Show current AI model
- `/models` - Show available AI models (Owner only)
- `/setmodel <name>` - Set AI model (Owner only)

### 💬 Smart Conversations
- Role-based responses using Cerebras AI
- Conversation memory (last 20 messages)
- Context-aware interactions
- Typing indicators for better UX

## 🚀 Quick Setup

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Cerebras API Key

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example file
copy env_example.txt .env

# Edit .env with your actual credentials
BOT_TOKEN=your_actual_telegram_bot_token
BOT_OWNER_ID=your_actual_telegram_user_id
CEREBRAS_API_KEY=your_actual_cerebras_api_key
```

### 3. Run the Bot
```bash
# Option 1: Direct run
python bot.py

# Option 2: Using startup script (recommended)
python start_bot.py
```

### 3. Get Your Credentials

#### Telegram Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command
3. Follow instructions to create your bot
4. Copy the provided token

#### Bot Owner ID
1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your user ID
3. Copy the user ID number

#### Cerebras API Key
1. Visit [Cerebras AI](https://cerebras.ai/)
2. Sign up for an account
3. Navigate to API section
4. Generate your API key

### 4. Run the Bot
```bash
python bot.py
```

## 🏗️ Project Structure

```
├── bot.py              # Main bot application
├── config.py           # Configuration and role definitions
├── cerebras_client.py  # Cerebras API client
├── user_manager.py     # User session management
├── start_bot.py        # Startup script with error checking
├── requirements.txt    # Python dependencies
├── env_example.txt    # Environment variables template
└── README.md          # This file
```

## 🎯 How It Works

1. **User Management**: Each user gets a unique session with role preferences
2. **Role Selection**: Users can switch between different AI personalities
3. **Context Memory**: Bot remembers conversation history for context
4. **API Integration**: Uses Cerebras AI for intelligent, role-based responses
5. **Dynamic Responses**: Bot adapts its tone and expertise based on selected role
6. **Model Management**: Bot owner can switch between available AI models

## 👑 Owner Features

### Model Management
- **View Available Models**: `/models` - See all available Cerebras AI models
- **Change AI Model**: `/setmodel <model_name>` - Switch to a different model
- **Current Model**: `/currentmodel` - Check which model is currently active

### Owner Commands
- Only the bot owner (configured via `BOT_OWNER_ID`) can access model management
- Models are fetched from the official Cerebras API endpoint
- Automatic validation ensures only valid models can be selected

## 🔒 Security Features

- Environment variable configuration
- API key validation
- User session isolation
- Conversation history limits
- Error handling and logging

## 🛠️ Customization

### Adding New Roles
Edit `config.py` to add new roles:
```python
"new_role": {
    "name": "New Role Name",
    "description": "Role description",
    "system_prompt": "Custom system prompt for this role"
}
```

### Modifying System Prompts
Each role has a customizable system prompt that defines its behavior and expertise.

## 📱 Usage Examples

### Starting a Conversation
```
User: /start
Bot: 👋 Hello [Name]! Welcome to your AI companion bot!
     I can adapt to different roles to better assist you...
```

### Changing Roles
```
User: /roles
Bot: 🎭 Choose Your AI Companion Role:
     [Default Assistant] [Code Expert] [Data Analyst]
     [Male Partner] [Female Partner] [Supportive Friend] [Therapeutic Support]
```

### Role-Specific Interactions
- **Code Expert**: Ask programming questions, get code examples
- **Data Analyst**: Discuss data insights, statistical concepts
- **Therapeutic Support**: Emotional guidance and coping strategies

## 🐛 Troubleshooting

### Common Issues

1. **"Cerebras API key not configured"**
   - Check your `.env` file
   - Ensure `CEREBRAS_API_KEY` is set correctly

2. **"Bot token not configured"**
   - Verify your Telegram bot token in `.env`
   - Ensure bot is created with @BotFather

3. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

4. **"I'm sorry, I encountered an error: 404"**
   - This means the Cerebras API endpoint is not found
   - Run the API test: `python test_api.py`
   - Check if your Cerebras API key is valid
   - Verify the API endpoints at https://cerebras.ai/
   - The bot will now provide fallback responses when API is unavailable

### API Connection Issues

If you're getting 404 errors with the Cerebras API:

1. **Test your API connection:**
   ```bash
   python test_api.py
   ```

2. **Check your API key:**
   - Visit [Cerebras AI](https://cerebras.ai/)
   - Verify your API key is active and valid
   - Ensure you have sufficient credits/quota

3. **Alternative solutions:**
   - The bot now has fallback responses when API is down
   - Each role will still respond appropriately even without AI
   - Check Cerebras service status

### Getting Help
- Check the logs for detailed error messages
- Verify your API credentials
- Ensure all dependencies are installed
- Run `python test_setup.py` to diagnose issues
- Run `python test_api.py` to test API connection

## 🤝 Contributing

Feel free to contribute by:
- Adding new roles
- Improving error handling
- Enhancing the UI/UX
- Adding new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Cerebras AI](https://cerebras.ai/) - AI model API
- Telegram Bot API for the platform

---

**Happy chatting with your AI companions! 🎉** 