from mm_activity_service.config.config import Config
from mm_activity_service.app import create_app, register_consul


def run():
    app = create_app()
    config = Config()

    register_consul()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )