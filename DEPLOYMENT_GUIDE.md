# 🚀 Telegram Bot Deployment Guide

This guide will help you deploy your Telegram bot on various platforms.

## 📋 Prerequisites

1. **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather)
2. **Cerebras API Key** - Get from [Cerebras AI](https://cerebras.ai/)
3. **GitHub Account** - For code hosting

## 🎯 Quick Start (Local)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
BOT_TOKEN=your_telegram_bot_token_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
BOT_OWNER_ID=your_telegram_user_id_here  # Optional
```

### 3. Run the Bot
```bash
python simple_bot.py
```

## ☁️ Cloud Deployment Options

### Option 1: Railway (Recommended)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Create new project** from GitHub repo
4. **Set environment variables:**
   - `BOT_TOKEN` = Your Telegram bot token
   - `CEREBRAS_API_KEY` = Your Cerebras API key
   - `BOT_OWNER_ID` = Your Telegram user ID (optional)
5. **Deploy** - Railway will automatically detect Python and run your bot

### Option 2: Render

1. **Sign up** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect GitHub** repository
4. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python simple_bot.py`
5. **Set environment variables** (same as Railway)
6. **Deploy**

### Option 3: Heroku

1. **Sign up** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**
3. **Create app:**
   ```bash
   heroku create your-bot-name
   ```
4. **Set environment variables:**
   ```bash
   heroku config:set BOT_TOKEN=your_token
   heroku config:set CEREBRAS_API_KEY=your_key
   heroku config:set BOT_OWNER_ID=your_id
   ```
5. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 4: Python Anywhere

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload your files** via Files tab
3. **Open Bash console**
4. **Install dependencies:**
   ```bash
   pip install --user -r requirements.txt
   ```
5. **Set environment variables** in console:
   ```bash
   export BOT_TOKEN=your_token
   export CEREBRAS_API_KEY=your_key
   export BOT_OWNER_ID=your_id
   ```
6. **Run bot:**
   ```bash
   python simple_bot.py
   ```

### Option 5: VPS/Server

1. **Get a VPS** (DigitalOcean, AWS, etc.)
2. **SSH into server**
3. **Install Python:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
4. **Clone repository:**
   ```bash
   git clone your-repo-url
   cd your-repo
   ```
5. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Set environment variables:**
   ```bash
   export BOT_TOKEN=your_token
   export CEREBRAS_API_KEY=your_key
   export BOT_OWNER_ID=your_id
   ```
7. **Run in background:**
   ```bash
   nohup python3 simple_bot.py > bot.log 2>&1 &
   ```

## 🔧 Required Files

Make sure your repository has these files:

```
your-repo/
├── simple_bot.py          # Main bot file
├── config.py              # Configuration
├── cerebras_client.py     # AI client
├── user_manager.py        # User management
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (local only)
└── README.md             # Documentation
```

## 🐛 Troubleshooting

### Common Issues

1. **"Bot not responding"**
   - Check if bot is running
   - Verify environment variables
   - Check bot token validity

2. **"API key not configured"**
   - Set `CEREBRAS_API_KEY` environment variable
   - Verify API key is valid

3. **"Import errors"**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+)

4. **"Connection timeout"**
   - Check internet connection
   - Verify API endpoints are accessible

### Environment Variables

Required:
```bash
BOT_TOKEN=your_telegram_bot_token_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

Optional:
```bash
BOT_OWNER_ID=your_telegram_user_id_here
```

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

1. **Push changes** to GitHub repository
2. **Platform will auto-deploy** (Railway, Render, Heroku)
3. **Manual restart** (VPS, Python Anywhere)

## 🆘 Support

If you encounter issues:

1. **Check logs** in your deployment platform
2. **Verify environment variables** are set correctly
3. **Test locally** first with `python simple_bot.py`
4. **Check bot token** with @BotFather

## 🎉 Success!

Once deployed:

1. **Your bot will be accessible** via Telegram
2. **Users can interact** with your bot
3. **Bot will run continuously** on your chosen platform
4. **Monitor logs** for any issues

---

**Happy deploying! 🚀**
