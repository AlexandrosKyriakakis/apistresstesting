import time

import requests

from config import enum
from config.config import Env
from config.logger import logger
from src.redpanda.admin import create_topics
from src.redpanda.consume import consume
from src.redpanda.produce import produce


def pubsub():
    cfg = Env()

    create_topics(cfg.RED_PANDA_TOPIC, cfg.RED_PANDA_BROKER_0)
    while True:
        if cfg.ROLE == enum.ROLE_RED_PANDA_CONSUMER:
            cons = consume(
                cfg.RED_PANDA_BROKER_0,
                [
                    cfg.RED_PANDA_TOPIC,
                ],
                cfg.RED_PANDA_CONSUMER_GROUP,
            )
            logger.info('consumed redpanda message: %s', next(cons))

        elif cfg.ROLE == enum.ROLE_RED_PANDA_PRODUCER:
            response = requests.get(cfg.EXTERNAL_HOST)
            logger.info('producing redpanda message: \n %s', str(response.content))
            produce(cfg.RED_PANDA_TOPIC, cfg.RED_PANDA_KEY, response.content, cfg)
            time.sleep(1)

        else:
            logger.error('wrong red panda role: %s', cfg.ROLE)
