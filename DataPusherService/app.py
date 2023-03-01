from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.pass_data import DataPushing
import config


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = 'secretkey'
    JWTManager(app)

    api.add_resource(DataPushing, '/send_data')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=False)
