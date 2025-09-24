import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# OpenAI API (deprecated)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Calendar
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_OAUTH_REDIRECT_PORT = int(os.getenv("GOOGLE_OAUTH_REDIRECT_PORT", "8088"))
GOOGLE_OAUTH_REDIRECT_PATH = os.getenv("GOOGLE_OAUTH_REDIRECT_PATH", "/oauth2callback")
GOOGLE_OAUTH_REDIRECT_BASE = os.getenv("GOOGLE_OAUTH_REDIRECT_BASE", "")  # если пусто, используем localhost

# Firebase
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "caloriesbot-949dd-firebase-adminsdk-fbsvc-4ecc1b1ad9.json")

# Temporary files directory
TEMP_DIR = "temp_photos"

# Logging
LOG_LEVEL = "INFO"
