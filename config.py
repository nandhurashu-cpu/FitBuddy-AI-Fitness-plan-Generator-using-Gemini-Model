import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# These can be changed in .env if your Google AI account exposes different models.
WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.7-flash")
TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-3.7-flash")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(BASE_DIR / 'fitbuddy.db').as_posix()}",
)
