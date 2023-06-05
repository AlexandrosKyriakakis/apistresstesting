import datetime

import orjson
import pika as pika
from epiweeks import Week

from config.config import Env
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_REST
from config.enum import ARCHITECTURE_RMQ
from src.postgres import Session
from src.postgres.models.my_model import WeeklyTotalLoad
from src.rmq.consume import consume
from src.rmq.produce import produce

cfg = Env()


def parse_data(ch, method, properties, body: bytes):
    data = orjson.loads(body)
    if len(data) == 0:
        return

    model = []
    area_ref = data[0]['city']
    date: datetime.date = datetime.datetime.fromisoformat(data[0]['date']).date()
    week = Week.fromdate(date).week
    total_week = 0
    for value in data:
        current_date: datetime.date = datetime.datetime.fromisoformat(
            value['date']
        ).date()
        # print(value)
        current_week = Week.fromdate(current_date).week
        if current_week == week:
            total_week += value['total_load']
        else:
            model.append(
                {
                    'city': area_ref,
                    'date': date,
                    'week': week,
                    'total_load': total_week,
                }
            )
            total_week = value['total_load']
            date = current_date
            week = current_week
    model.append(
        {
            'city': area_ref,
            'date': date,
            'week': week,
            'total_load': total_week,
        }
    )

    produce(ch, cfg.RMQ_QUEUE_NAME_MONTHLY, orjson.dumps(model))
    save_to_db(model)


def save_to_db(data_batch: list[dict]):
    session = Session()
    for d in data_batch:
        session.add(
            WeeklyTotalLoad(
                date=d['date'],
                country=d['city'],
                load=int(d['total_load']),
                week=d['week'],
            )
        )
    session.commit()
    session.close()


def rmq_flow():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_WEEKLY)
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_MONTHLY)

    consume(channel, cfg.RMQ_QUEUE_NAME_WEEKLY, parse_data)


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
