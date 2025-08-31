import logging

from flask import Flask, Blueprint
from flask_restx import Api
from mm_activity_service.config.logger import setup_logger
from mm_activity_service.config.config import Config
from mm_activity_service.config.db import MongoDBConnector
from mm_activity_service.preference.controller import ns as preference_ns
from mm_activity_service.watchlist.controller import ns as watchlist_ns
from mm_activity_service.rating.controller import ns as ratings_ns

config = Config()
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    setup_logger(config.LOG_LEVEL)

    app.env = config.ENV
    init_db()
    init_endpoints(app)
    return app


def init_endpoints(app: Flask):
    api_blueprint = Blueprint('api', __name__, url_prefix=config.BASE_URL)
    api = Api(
        api_blueprint,
        version="1.0",
        title="mm-activity-service",
        doc="/docs/swagger"
    )
    app.register_blueprint(api_blueprint)

    api.add_namespace(preference_ns)
    api.add_namespace(watchlist_ns)
    api.add_namespace(ratings_ns)


def init_db():
    db = MongoDBConnector(db_name=config.DB_NAME, host=config.DB_HOST, port=int(config.DB_PORT), username=None, password=None)
    if db.test_connection():
        logger.info("MongoDB connection established.")
    else:
        logger.error("MongoDB connection failed.")