import asyncio
import datetime
import time

import orjson
import pika as pika
import websockets

from config.config import Env
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_REST_ORCHESTRATOR
from config.enum import ARCHITECTURE_RMQ
from src.postgres import Session
from src.postgres.models.my_model import DailyTotalLoad
from src.prometheus.prometheus import DAILY_FORWARD_TIME
from src.prometheus.prometheus import DAILY_PARSE_TIME
from src.prometheus.prometheus import DAILY_SAVE_TIME
from src.prometheus.prometheus import FINAL_DELAY
from src.prometheus.prometheus import time_histogram
from src.redpanda.consume import consume as rpk_consume
from src.rmq.consume import consume as rmq_consume
from src.rmq.produce import produce as rmq_produce


cfg = Env()


@time_histogram(DAILY_FORWARD_TIME)
def forward_data(ch, method, properties, body: bytes):
    # start = time.time()
    model = parse_data(body)
    rmq_produce(ch, cfg.RMQ_QUEUE_NAME_WEEKLY, orjson.dumps(model))
    save_to_db(model)
    # end -
    # pprint(model)  # TODO REMOVE


@time_histogram(DAILY_PARSE_TIME)
def parse_data(body: bytes) -> list[dict]:
    data = orjson.loads(body)
    if len(data['data']['TotalLoad']) == 0:
        return []

    model = []
    area_ref = data['meta']['requestParams']['areaRefAbbrev']
    date: datetime.date = datetime.datetime.fromisoformat(
        data['data']['TotalLoad'][0]['DateTime'][:-1]
    ).date()
    total_day = 0
    for value in data['data']['TotalLoad']:
        current_date = datetime.datetime.fromisoformat(value['DateTime'][:-1]).date()
        if current_date == date:
            total_day += value['value']
        else:
            model.append({'city': area_ref, 'date': date, 'total_load': total_day})
            total_day = value['value']
            date = current_date
    model.append({'city': area_ref, 'date': date, 'total_load': total_day})
    return model


@time_histogram(DAILY_SAVE_TIME)
def save_to_db(data_batch: list[dict]):
    session = Session()
    for d in data_batch:
        session.add(
            DailyTotalLoad(date=d['date'], country=d['city'], load=int(d['total_load']))
        )
    session.commit()
    session.close()


def rmq_flow():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_DAILY)
    channel.queue_declare(queue=cfg.RMQ_QUEUE_NAME_WEEKLY)

    rmq_consume(channel, cfg.RMQ_QUEUE_NAME_DAILY, forward_data)


def red_panda_flow():
    for data in rpk_consume(
        cfg.RED_PANDA_BROKER_0, [cfg.RED_PANDA_TOPIC], cfg.RED_PANDA_CONSUMER_GROUP
    ):
        model = parse_data(data.value)
        if model:
            save_to_db(model)
            # End point for metrics
            current_time_micros = time.time_ns()
            FINAL_DELAY.labels(
                country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
            ).set(current_time_micros)


def rest_orchestrator_flow():
    async def server(websocket, path):
        data: bytes = await websocket.recv()
        model = parse_data(data)
        save_to_db(model)
        await websocket.send(orjson.dumps(model))

    start_server = websockets.serve(server, '0.0.0.0', cfg.WSS_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def run():
    if cfg.ARCHITECTURE == ARCHITECTURE_RMQ:
        rmq_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_REST_ORCHESTRATOR:
        rest_orchestrator_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_REDPANDA:
        red_panda_flow()
    else:
        raise ModuleNotFoundError
