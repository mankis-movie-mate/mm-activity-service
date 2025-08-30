import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    _ENV_PREFIX = "MOVIE_MATE_ACTIVITY_SERVICE_"

    def __init__(self):
        self.ENV = os.getenv(f"{self._ENV_PREFIX}ENV", "dev")
        self.DEBUG = os.getenv(f"{self._ENV_PREFIX}DEBUG", "true")
        self.PORT = os.getenv(f"{self._ENV_PREFIX}PORT", "5000")
        self.HOST = os.getenv(f"{self._ENV_PREFIX}HOST", "0.0.0.0")
        self.BASE_URL = os.getenv(f"{self._ENV_PREFIX}BASE_URL", "/api/v1")
        self.DB_NAME = os.getenv(f"{self._ENV_PREFIX}DB_NAME")
        self.DB_HOST = os.getenv(f"{self._ENV_PREFIX}DB_HOST")
        self.DB_PORT = os.getenv(f"{self._ENV_PREFIX}DB_PORT", "27017")
        self.DB_USER = os.getenv(f"{self._ENV_PREFIX}DB_USER")
        self.DB_PASSWORD = os.getenv(f"{self._ENV_PREFIX}DB_PASSWORD")
        self.LOG_LEVEL = os.getenv(f"{self._ENV_PREFIX}LOG_LEVEL", "INFO")