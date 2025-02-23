from flask import Flask
from flask_restx import Api
from src.config.config import Config

config = Config()


def create_app() -> Flask:
    app = Flask(__name__)
    app.env = config.ENV
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