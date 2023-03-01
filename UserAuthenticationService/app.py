from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from resources.user import Register, Login
import config


def create_app():
    app = Flask(__name__)
    api = Api(app)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Python logger application"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    app.config['JWT_SECRET_KEY'] = 'secretkey'
    JWTManager(app)

    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=False)
