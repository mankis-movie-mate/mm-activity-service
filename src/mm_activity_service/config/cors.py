from flask import Flask
from flask_cors import CORS
from mm_activity_service.config.config import Config


def configure_cors(app: Flask, config: Config):
    base_path = config.BASE_URL
    if not base_path.startswith("/"):
        base_path = "/" + base_path
    if not base_path.endswith("/"):
        base_path += "/"

    cors_path = rf"{base_path}*"  # Regex-compatible path: /api/*

    print(f"🔗 CORS: Exposing {cors_path} to origins = {config.ALLOWED_ORIGINS}")

    CORS(
        app,
        resources={
            cors_path: {
                "origins": config.ALLOWED_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            }
        },
        supports_credentials=True,
    )
