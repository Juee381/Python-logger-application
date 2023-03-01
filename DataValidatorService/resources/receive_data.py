import random
import time
from datetime import datetime, date

import pika
import ast
import requests

import config


class RabbitmqConfigure:

    def __init__(self, host=config.RABBITMQ_HOST, queue=config.RABBITMQ_QUEUE_NAME):
        """ Server initialization   """

        self.host = host
        self.queue = queue


class RabitMq:

    def __init__(self, consumer):
        """
        :param consumer: Object of class RabbitmqConfigure
        """

        self.consumer = consumer
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.consumer.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.consumer.queue)
        print("Server started waiting for Messages ")

    @staticmethod
    def callback(ch, method, properties, body):
        payload = body.decode("utf-8")
        payload = ast.literal_eval(payload)  # give dictionary type data otherwise got str type

        for data in payload.values():
            if data['random_num'] % 10 == 0:
                data['category'] = "Retried"
                data['random_num'] = random.randint(1, 60)

                #after 4 sec
                time.sleep(4)

                if data['random_num'] % 10 == 0:
                    data['category'] = "Failed"
                else:
                    data['category'] = "Direct"
            else:
                data['category'] = "Direct"

            data['created_time'] = str(datetime.now())

        response = requests.post("http://localhost:5061/data", json=payload)
        print(response.status_code)

        print(type(payload))
        print("Data Received : {}".format(payload))

    def startConsumer(self):
        self._channel.basic_consume(
            queue=self.consumer.queue,
            on_message_callback=RabitMq.callback,
            auto_ack=True)
        self._channel.start_consuming()


# class DataValidator(Resource):
#     @classmethod
#     def get(cls):
#         consumer = RabbitmqConfigure(host=config.RABBITMQ_HOST, queue=config.RABBITMQ_QUEUE_NAME)
#         rabbitmq = RabitMq(consumer=consumer)
#         rabbitmq.startConsumer()

if __name__ == "__main__":
    serverconfigure = RabbitmqConfigure(host=config.RABBITMQ_HOST,
                                        queue=config.RABBITMQ_QUEUE_NAME)

    server = RabitMq(consumer=serverconfigure)
    server.startConsumer()
