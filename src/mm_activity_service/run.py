from mm_activity_service.config.config import Config
from mm_activity_service.app import create_app


def run():
    app = create_app()
    config = Config()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )