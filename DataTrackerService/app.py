from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.data_tracker import Insert_data, Fetch_user_msg, Msg_count_by_category_date, Msg_count_by_category, Msg_count_by_date


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = 'secretkey'
    JWTManager(app)

    api.add_resource(Insert_data, '/data')
    api.add_resource(Fetch_user_msg, '/fetch_msg')
    api.add_resource(Msg_count_by_category_date, '/msg_count_by_category_date')
    api.add_resource(Msg_count_by_category, '/msg_count_by_category')
    api.add_resource(Msg_count_by_date, '/msg_count_by_date')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='localhost', port=5061, debug=False)
