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

# Temporary files directory
TEMP_DIR = "temp_photos"

# Logging
LOG_LEVEL = "INFO"
