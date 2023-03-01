from elasticsearch import Elasticsearch, helpers
from datetime import datetime

elastic_client = Elasticsearch(hosts='http://localhost:9200')


class Elasticsearch_fun():
    def __init__(self):
        pass

    def create_index(self):
        body = {}
        is_exists = elastic_client.indices.exists(index="data_tracker")

        if not is_exists:
            elastic_client.indices.create(index="data_tracker", body=body, ignore=400)

    def insert_data(self, result):
        # elastic_client.bulk(index="data_tracker", operations=result)
        for data in result.values():
            print(data)
            print(type(data))
            elastic_client.index(index="data_tracker", document=data)

        # rows = []
        # print("i")
        # for data in result:
        #     rows.append(
        #         {
        #             '_index': "data_tracker",
        #             '_source': data
        #         }
        #     )
        # response = helpers.bulk(elastic_client, operations=rows, request_timeout=30)
        # print(response)
        return result

    def get_all_users(self):
        search_param = {
            'query': {
                'match_all': {}
            }
        }
        result = elastic_client.search(index="data_tracker", size=100, body=search_param)
        return result

    def search_selective_msg(self, text):
        search_param = {
            'query': {
                'match': {
                    'user_msg': text
                }
            }
        }
        response = elastic_client.search(index="data_tracker", body=search_param)
        print(response)
        return response

    def num_of_msg_by_category_date(self, category, date):
        search_param = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'match': {
                                'category': category
                            }
                        },
                        {
                            'match': {
                                'created_time': {
                                    'query': date,
                                    'operator': 'and'
                                }
                            }
                        }
                    ]
                }
            }
        }
        response = elastic_client.count(index="data_tracker", body=search_param)
        print(response)
        return response

    def num_of_msg_by_category(self, category):
        search_param = {
            'query': {
                'match': {
                    "category": category
                }
            }
        }
        response = elastic_client.count(index="data_tracker", body=search_param)
        return response

    def num_of_msg_by_date(self, date):
        search_param = {
            'query': {
                'match': {
                    'created_time': {
                        'query': date,
                        'operator': 'and'
                    }
                }
            }
        }
        response = elastic_client.count(index="data_tracker", body=search_param)
        print(response)
        return response
