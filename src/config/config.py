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