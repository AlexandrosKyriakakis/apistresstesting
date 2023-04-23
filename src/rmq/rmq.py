import time

import pika
import requests
from config import enum
from config.config import Env
from config.logger import logger
from src.rmq.consume import consume
from src.rmq.produce import produce


def callback(ch, method, properties, body):
    logger.info('consumed rabbitmq message: %s', body.decode())


def rmq():
    cfg = Env()
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    # Create a queue named "hello"
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME)

    while True:
        if cfg.ROLE == enum.ROLE_RMQ_CONSUMER:
            # This will block here
            consume(channel, cfg.RMQ_QUEUE_NAME, callback)

        elif cfg.ROLE == enum.ROLE_RMQ_PRODUCER:
            response = requests.get(cfg.EXTERNAL_HOST)
            produce(channel, cfg.RMQ_QUEUE_NAME, response.content)
            logger.info('produced RMQ message: \n %s', str(response.content))
            time.sleep(1)

        else:
            logger.error('wrong RMQ role: %s', cfg.ROLE)

    # Close the connection
    # connection.close()
