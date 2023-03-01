from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_smorest import abort

import pika
from pika import exceptions
import random

from common.redis_config import redis_client
from common.constant import REDIS_COMMUNICATION_ERROR, REBBITMQ_CONNECTION_ERROR, REBBITMQ_MSG_SENDING_ERROR, \
    REBBITMQ_MSG_SEND, INVALID_TOKEN
import config

class RabbitmqConfigure:

    def __init__(self, queue='data', host=config.RABBITMQ_HOST, routingKey='data', exchange=''):
        """ Configure Rabbit Mq consumer  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMq():

    def __init__(self, consumer):
        """
        :param consumer: Object of class RabbitmqConfigure
        """

        self.consumer = consumer

        try:
            self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.consumer.host))
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self.consumer.queue)
        except:
            abort(500, message=REBBITMQ_CONNECTION_ERROR)

    def publish(self, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """
        try:
            self._channel.basic_publish(exchange='', routing_key=self.consumer.routingKey,
                                        body=str(payload))
        except pika.exceptions.ChannelClosed as err:
            abort(500, message=err)
        except pika.exceptions.ConnectionClosed as err:
            abort(500, message=err)
        except:
            abort(500, message=REBBITMQ_MSG_SENDING_ERROR)
        # return {"message": REBBITMQ_MSG_SEND}, 201

        print("Published Message: {}".format(payload))

        self._connection.close()


class DataPushing(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        user_id = get_jwt_identity()
        request_data = request.get_json()

        id_counter = user_id + "_counter"
        try:
            if user_id:
                cnt = redis_client.hget("counter", id_counter)
                if cnt:
                    redis_client.hset("counter", id_counter, int(cnt) + 1)
                else:
                    redis_client.hset("counter", id_counter, 1)
            else:
                return {"message": INVALID_TOKEN}, 403

        except:
            abort(500, REDIS_COMMUNICATION_ERROR)

        request_counter = int(redis_client.hget("counter", id_counter))

        for data in request_data.values():
            print(type(data))
            data["user_id"] = user_id
            data["random_num"] = random.randint(1, 60)
            data["request_counter"] = request_counter
            print(data)

        consumer = RabbitmqConfigure(queue='data',
                                     host='localhost',
                                     routingKey='data',
                                     exchange='')

        rabbitmq = RabbitMq(consumer)
        rabbitmq.publish(payload=request_data)
