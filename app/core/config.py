from cli.config.config import Config
from dotenv import load_dotenv
import os

class Config(Config):

    load_dotenv()

    APP_TIMEZONE = os.getenv("APP_TIMEZONE", "Asia/Jakarta")