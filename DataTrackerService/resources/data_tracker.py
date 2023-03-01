from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from es import Elasticsearch_fun

es_fun = Elasticsearch_fun()
es_fun.create_index()


class Insert_data(Resource):
    def post(self):
        res = request.get_json()
        print(res)
        print(type(res))

        try:
            Elasticsearch_fun.insert_data(self, res)
            print("inserted")
            return {"Inserted data": res}, 201
        except Exception as err:
            return err

    @jwt_required(fresh=True)
    def get(self):
        result = Elasticsearch_fun.get_all_users(self)
        print(type(result))
        d = dict(result)
        print(type(d))

        result = []
        for i in range(0, len(d['hits']['hits'])):
            result.append(d['hits']['hits'][i]['_source'])

        return result


class Fetch_user_msg(Resource):
    @jwt_required(fresh=True)
    def get(self):
        text = request.args.get("text")
        print(text)

        try:
            result = Elasticsearch_fun.search_selective_msg(self, text)
            print(type(result))
            d = dict(result)
            print(type(d))
            print(result)

            result = []
            for i in range(0, len(d['hits']['hits'])):
                result.append(d['hits']['hits'][i]['_source'])

            return result
        except Exception as err:
            return err


class Msg_count_by_category_date(Resource):
    @jwt_required(fresh=True)
    def get(self):
        category = request.args.get("category")
        date = request.args.get("date")

        try:
            result = Elasticsearch_fun.num_of_msg_by_category_date(self, category, date)

            d = dict(result)
            return d['count']

        except Exception as err:
            return err


class Msg_count_by_category(Resource):
    @jwt_required(fresh=True)
    def get(self):
        category = request.args.get("category")
        print(category)
        try:
            result = Elasticsearch_fun.num_of_msg_by_category(self, category)  # type: ObjectApiResponse
            d = dict(result)
            return d['count']
        except Exception as err:
            return err


class Msg_count_by_date(Resource):

    @jwt_required(fresh=True)
    def get(self):
        date = request.args.get("date")
        try:
            result = Elasticsearch_fun.num_of_msg_by_date(self, date)
            d = dict(result)
            return d['count']
        except Exception as err:
            return {"message": err}
