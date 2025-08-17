# 🚀 Streamlit Deployment Guide

This guide will help you deploy your Telegram bot on Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Streamlit Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather)
4. **Cerebras API Key** - Get from [Cerebras AI](https://cerebras.ai/)

## 🔧 Setup Steps

### 1. Prepare Your Repository

Make sure your repository has these files:
```
├── streamlit_bot.py          # Main Streamlit app
├── bot_streamlit.py          # Streamlit-optimized bot
├── config.py                 # Configuration
├── cerebras_client.py        # AI client
├── user_manager.py           # User management
├── requirements_streamlit.txt # Dependencies
├── .streamlit/config.toml    # Streamlit config
└── README.md                 # Documentation
```

### 2. Configure Environment Variables

In your Streamlit Cloud dashboard:

1. Go to your app settings
2. Add these environment variables:
   - `BOT_TOKEN` = Your Telegram bot token
   - `CEREBRAS_API_KEY` = Your Cerebras API key
   - `BOT_OWNER_ID` = Your Telegram user ID (optional)

### 3. Deploy on Streamlit

1. **Connect GitHub Repository:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository

2. **Configure App:**
   - **Main file path:** `streamlit_bot.py`
   - **Python version:** 3.9 or higher
   - **Requirements file:** `requirements_streamlit.txt`

3. **Deploy:**
   - Click "Deploy!"
   - Wait for deployment to complete

## 🎯 Usage

1. **Access Your Dashboard:**
   - Open the Streamlit app URL
   - You'll see the bot dashboard

2. **Start the Bot:**
   - Click "🚀 Start Bot" in the sidebar
   - The bot will begin polling for messages

3. **Monitor Status:**
   - The dashboard shows bot status
   - View available roles and commands
   - Monitor bot activity

## 🔍 Troubleshooting

### Common Issues

1. **"Updater object has no attribute '_Updater__polling_cleanup_cb'"**
   - ✅ **FIXED:** Use `bot_streamlit.py` instead of `bot.py`
   - This version has Streamlit-compatible settings

2. **"BOT_TOKEN not configured"**
   - Check environment variables in Streamlit Cloud
   - Ensure `BOT_TOKEN` is set correctly

3. **"CEREBRAS_API_KEY not configured"**
   - Add your Cerebras API key to environment variables
   - Verify the key is valid

4. **Import errors**
   - Check `requirements_streamlit.txt` has all dependencies
   - Ensure Python version is 3.9+

### Environment Variables

Make sure these are set in Streamlit Cloud:

```bash
BOT_TOKEN=your_telegram_bot_token_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
BOT_OWNER_ID=your_telegram_user_id_here  # Optional
```

### File Structure

Your repository should look like this:

```
your-repo/
├── streamlit_bot.py          # Main Streamlit app
├── bot_streamlit.py          # Bot implementation
├── config.py                 # Configuration
├── cerebras_client.py        # AI client
├── user_manager.py           # User management
├── requirements_streamlit.txt # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit settings
└── README.md                # Documentation
```

## 🎉 Success!

Once deployed:

1. **Your bot will be accessible via the Streamlit URL**
2. **Users can interact with your bot on Telegram**
3. **You can monitor bot activity through the dashboard**
4. **The bot will run continuously on Streamlit's servers**

## 📱 Bot Features

Your deployed bot includes:

- **7 Different AI Personalities** (Default, Code Expert, Data Analyst, etc.)
- **Role-based Responses** with unique personalities
- **Conversation Memory** (last 20 messages)
- **Partner Roles** with customizable names
- **Model Management** (owner only)
- **Real-time Status Monitoring**

## 🔄 Updates

To update your bot:

1. Push changes to your GitHub repository
2. Streamlit will automatically redeploy
3. The bot will restart with new features

## 🆘 Support

If you encounter issues:

1. Check the Streamlit logs in your dashboard
2. Verify environment variables are set correctly
3. Ensure all dependencies are in `requirements_streamlit.txt`
4. Test locally first with `streamlit run streamlit_bot.py`

---

**Happy deploying! 🚀**
