from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    from api.v1 import v1_blueprint
    app.register_blueprint(v1_blueprint)

    CORS(app)
    return app
