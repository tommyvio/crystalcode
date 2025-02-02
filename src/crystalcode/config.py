import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-neo-125M")
    MAX_LENGTH = int(os.getenv("MAX_LENGTH", "200"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    API_PORT = int(os.getenv("API_PORT", "5000"))
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
