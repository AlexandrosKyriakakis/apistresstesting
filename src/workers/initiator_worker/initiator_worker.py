import time

import pika

from config.config import Env
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_REST_ORCHESTRATOR
from config.enum import ARCHITECTURE_RMQ
from src.postgres.init_db import init_db
from src.redpanda.admin import create_topics


def init_rmq(cfg: Env):
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME)
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_DAILY)
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_WEEKLY)
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_MONTHLY)


def init_rpk(cfg: Env):
    create_topics(cfg.RED_PANDA_TOPIC, cfg.RED_PANDA_BROKER_0)


def run():
    time.sleep(10)

    cfg = Env()
    init_db()

    if cfg.ARCHITECTURE == ARCHITECTURE_REDPANDA:
        init_rpk(cfg)
        return
    elif cfg.ARCHITECTURE == ARCHITECTURE_RMQ:
        init_rmq(cfg)
        return
    elif cfg.ARCHITECTURE == ARCHITECTURE_REST_ORCHESTRATOR:
        pass
    else:
        raise ModuleNotFoundError
