from flask import Flask
from flask_restful import Api
# from resources.receive_data import DataValidator


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # api.add_resource(DataValidator, '/validate_data')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='localhost', port=5060, debug=False)
