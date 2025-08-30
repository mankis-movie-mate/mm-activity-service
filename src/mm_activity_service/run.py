from mm_activity_service.config.config import Config
from app import create_app


if __name__ == "__main__":
    app = create_app()
    config = Config()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )