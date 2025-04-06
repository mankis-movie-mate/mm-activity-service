import logging
from flask import Flask
from flask_restx import Api
from src.config.logger import LoggerConfig
from src.config.config import Config
from src.config.db import MongoDB

config = Config()


def create_app() -> Flask:
    app = Flask(__name__)
    LoggerConfig.init_logger(app, config.LOG_LEVEL)

    app.env = config.ENV
    init_db(app)
    init_swagger(app)

    return app


def init_swagger(app: Flask):
    api = Api(
        app, 
        version="1.0", 
        title="mm-activity-service",
        prefix=config.BASE_URL, 
        doc="/swagger-ui"
    )

    from .controller.hello_controller import ns as hello_namespace
    api.add_namespace(hello_namespace)


def init_db(app: Flask):
    db = MongoDB(db_name=config.DB_NAME, host=config.DB_HOST, port=config.DB_PORT)
    if db.test_connection():
        app.logger.info("MongoDB connection established.")
    else:
        app.logger.error("MongoDB connection failed.")