import os

from pathlib import Path

from dotenv import load_dotenv


# Load .env file

load_dotenv()


# Project directory

BASE_DIR = Path(__file__).resolve().parent


# Gemini API Key

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


# Gemini model

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
).strip()


# Optional local explanation model

USE_LOCAL_EXPLANATION = os.getenv(
    "USE_LOCAL_EXPLANATION",
    "false"
).lower() in {
    "1",
    "true",
    "yes",
    "on"
}


LOCAL_MODEL_NAME = os.getenv(
    "LOCAL_MODEL_NAME",
    "MBZUAI/LaMini-Flan-T5-783M"
)