import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = str(os.getenv("TELEGRAM_TOKEN"))

ADMINS = os.getenv("TELEGRAM_ADMINS").split(",")

SERVICE_ACCOUNT = os.path.join("estate_bot/auth/", os.getenv("GOOGLE_SERVICE_ACCOUNT"))
SPREADSHEET_URL = os.getenv("GOOGLE_SPREADSHEET_URL")
