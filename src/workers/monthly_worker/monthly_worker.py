import datetime
import time

import orjson
import pika as pika

from config.config import Env
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_REST
from config.enum import ARCHITECTURE_RMQ
from src.postgres import Session
from src.postgres.models.my_model import MonthlyTotalLoad
from src.prometheus.prometheus import FINAL_DELAY
from src.rmq.consume import consume

cfg = Env()


def parse_data(ch, method, properties, body: bytes):
    data = orjson.loads(body)
    if len(data) == 0:
        return

    model = []
    area_ref = data[0]['city']
    date: datetime.date = datetime.datetime.fromisoformat(data[0]['date']).date()
    total_monthly = 0
    for value in data:
        total_monthly += value['total_load']
    model.append(
        {
            'city': area_ref,
            'date': date,
            'month': date.month,
            'total_load': total_monthly,
        }
    )

    save_to_db(model)

    # End point for metrics
    current_time_micros = time.time_ns()
    FINAL_DELAY.labels(country=area_ref, date=date.strftime('%Y-%m-%d')).set(
        current_time_micros
    )


def save_to_db(data_batch: list[dict]):
    session = Session()
    for d in data_batch:
        session.add(
            MonthlyTotalLoad(
                date=d['date'],
                country=d['city'],
                load=int(d['total_load']),
                month=d['month'],
            )
        )
    session.commit()
    session.close()


def rmq_flow():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_MONTHLY)

    consume(channel, cfg.RMQ_QUEUE_NAME_MONTHLY, parse_data)


def run():
    if cfg.ARCHITECTURE == ARCHITECTURE_RMQ:
        rmq_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_REST:
        raise NotImplemented
    elif cfg.ARCHITECTURE == ARCHITECTURE_REDPANDA:
        raise NotImplemented
    else:
        raise ModuleNotFoundError


# # TODO Make it async
# if __name__ == '__main__':
#     cfg = Env()
#     run()
