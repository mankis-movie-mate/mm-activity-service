import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    def __init__(self):
        self.ENV = os.getenv("ENV")
        self.DEBUG = os.getenv("DEBUG")
        self.PORT = os.getenv("PORT")
        self.HOST = os.getenv("HOST")
        self.BASE_URL = os.getenv("BASE_URL")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL")