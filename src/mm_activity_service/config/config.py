import os
import socket
import threading
from dotenv import load_dotenv
load_dotenv()


class Config:
    _MM_PREFIX = "MOVIE_MATE_"
    _ENV_PREFIX = "MOVIE_MATE_ACTIVITY_SERVICE_"
    _DAPR_PREFIX = f"{_ENV_PREFIX}DAPR_"
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        self.ENV = os.getenv(f"{self._ENV_PREFIX}ENV")
        self.DEBUG = os.getenv(f"{self._ENV_PREFIX}DEBUG") == 'true'
        self.PORT = os.getenv(f"{self._ENV_PREFIX}PORT")
        self.HOST = os.getenv(f"{self._ENV_PREFIX}APP_BIND_HOST", "0.0.0.0")
        self.LISTEN_HOST = os.getenv(f"{self._ENV_PREFIX}LISTEN_HOST", "127.0.0.1")
        self.BASE_URL = os.getenv(f"{self._ENV_PREFIX}BASE_URL")
        self.DB_NAME = os.getenv(f"{self._ENV_PREFIX}DB_NAME")
        self.ALLOWED_ORIGINS = os.getenv(f"{self._ENV_PREFIX}ALLOWED_ORIGINS", "*")
        self.DB_HOST = os.getenv(f"{self._ENV_PREFIX}DB_HOST")
        self.DB_PORT = os.getenv(f"{self._ENV_PREFIX}DB_PORT")
        self.DB_USER = os.getenv(f"{self._ENV_PREFIX}DB_USER")
        self.DB_PASSWORD = os.getenv(f"{self._ENV_PREFIX}DB_PASSWORD")
        self.DS_HOST = os.getenv(f"{self._MM_PREFIX}DISCOVERY_SERVER_HOST")
        self.DS_PORT = os.getenv(f"{self._MM_PREFIX}DISCOVERY_SERVER_PORT")
        self.LOG_LEVEL = os.getenv(f"{self._ENV_PREFIX}LOG_LEVEL")
        self.LB_TAGS = os.getenv(f"{self._ENV_PREFIX}LB_TAGS")

        # --- Dapr envs for pub/sub event publishing ---
        self.EVENTS_ENABLED = str(os.getenv(f"{self._ENV_PREFIX}EVENTS_ENABLED", "true")).lower() == "true"
        self.DAPR_HOST = os.getenv(f"{self._DAPR_PREFIX}HOST", "127.0.0.1")
        self.DAPR_HTTP_PORT = int(os.getenv(f"{self._DAPR_PREFIX}HTTP_PORT", "3500"))
        self.DAPR_PUBSUB_NAME = os.getenv(f"{self._DAPR_PREFIX}PUBSUB_NAME", "messagebus")
        self.DAPR_PUBSUB_TOPIC = os.getenv(f"{self._DAPR_PREFIX}PUBSUB_TOPIC", "user-activity")
        self.DAPR_PUBSUB_RAWPAYLOAD = os.getenv(f"{self._DAPR_PREFIX}PUBSUB_RAWPAYLOAD", "true").lower() == "true"