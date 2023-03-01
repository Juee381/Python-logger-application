import json

from flask_restful import Resource
from flask import request
from flask_smorest import abort
from flask_jwt_extended import create_access_token

import re
import uuid
from passlib.hash import pbkdf2_sha256

from common.redis_config import redis_client
from common.constant import USER_CREATED_SUCCESSFULLY, USER_ALREADY_EXISTS, INVALID_USERNAME, INVALID_PASSWORD, \
    PASSWORD_NOT_MATCH, USER_NOT_EXISTS


class Register(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()

        username = data["username"]
        password = data["password"]

        is_valid_username = re.match("^[a-zA-Z0-9_]{5,15}$", username)
        is_valid_password = re.match("^[a-zA-Z0-9!@#$%_]{6,12}$", password)

        random_user_id = str(uuid.uuid4())
        data["id"] = random_user_id

        if is_valid_username:
            if is_valid_password:
                # data["password"] = pbkdf2_sha256.hash(data["password"])
                key = username + "_data"
                if not redis_client.get(key):
                    str_data = json.dumps(data)
                    redis_client.set(key, str_data)
                    return {"message": USER_CREATED_SUCCESSFULLY}, 201
                abort(409, message=USER_ALREADY_EXISTS)
            abort(400, message=INVALID_PASSWORD)
        abort(400, message=INVALID_USERNAME)


class Login(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        key = username + "_data"
        redis_data = redis_client.get(key)
        json_data = json.loads(redis_data)

        print(json_data["id"])

        if redis_data:
            # if pbkdf2_sha256.verify(password, json_data["password"]):
            if password == json_data["password"]:
                access_token = create_access_token(identity=json_data["id"], fresh=True)
                return {"access_token": access_token}
            abort(401, message=PASSWORD_NOT_MATCH)
        abort(401, message=USER_NOT_EXISTS)
