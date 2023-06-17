import asyncio
import datetime
import sys
import time

import orjson
import pika as pika
import websockets

from config.config import Env
from config.enum import ARCHITECTURE_ASYNC_ORCHESTRATOR
from config.enum import ARCHITECTURE_ORCHESTRATOR
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_RMQ
from config.enum import ARCHITECTURE_SERIALISED_ORCHESTRATOR
from src.postgres import Session
from src.postgres.models.my_model import MonthlyTotalLoad
from src.prometheus.prometheus import async_time_histogram
from src.prometheus.prometheus import FINAL_DELAY
from src.prometheus.prometheus import MONTHLY_FORWARD_TIME
from src.prometheus.prometheus import MONTHLY_PARSE_TIME
from src.prometheus.prometheus import MONTHLY_SAVE_TIME
from src.prometheus.prometheus import MONTHLY_TOTAL_BYTES_AFTER_PROCESS
from src.prometheus.prometheus import MONTHLY_TOTAL_BYTES_RECEIVED
from src.prometheus.prometheus import MONTHLY_TOTAL_REQUESTS_PROCESSED
from src.prometheus.prometheus import time_histogram
from src.redpanda.consume import consume as rpk_consume
from src.rmq.consume import consume as rmq_consume

cfg = Env()


@time_histogram(MONTHLY_FORWARD_TIME)
def forward_data(ch, method, properties, body: bytes):
    model = parse_data(body)

    if model:
        save_to_db(model)

        # End point for metrics
        current_time_micros = time.time_ns()
        FINAL_DELAY.labels(
            country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
        ).set(current_time_micros)


@time_histogram(MONTHLY_PARSE_TIME)
def parse_data_rpk(body: bytes) -> list[dict]:
    MONTHLY_TOTAL_BYTES_RECEIVED.inc(sys.getsizeof(body))
    MONTHLY_TOTAL_REQUESTS_PROCESSED.inc()

    data = orjson.loads(body)
    if len(data['data']['TotalLoad']) == 0:
        return []

    model = []
    area_ref = data['meta']['requestParams']['areaRefAbbrev']
    date: datetime.date = datetime.datetime.fromisoformat(
        data['data']['TotalLoad'][0]['DateTime'][:-1]
    ).date()
    total_monthly = 0
    for value in data['data']['TotalLoad']:
        total_monthly += value['value']
    model.append(
        {
            'city': area_ref,
            'date': date,
            'month': date.month,
            'total_load': total_monthly,
        }
    )
    return model


@time_histogram(MONTHLY_PARSE_TIME)
def parse_data(body: bytes) -> list[dict]:
    MONTHLY_TOTAL_BYTES_RECEIVED.inc(sys.getsizeof(body))
    MONTHLY_TOTAL_REQUESTS_PROCESSED.inc()

    data = orjson.loads(body)
    if len(data) == 0:
        return []

    model = []
    area_ref = data[0]['city']
    date: datetime.date = datetime.datetime.fromisoformat(str(data[0]['date'])).date()
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
    return model


@time_histogram(MONTHLY_SAVE_TIME)
def save_to_db(data_batch: list[dict]):
    MONTHLY_TOTAL_BYTES_AFTER_PROCESS.inc(sys.getsizeof(data_batch))
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
    rmq_consume(channel, cfg.RMQ_QUEUE_NAME_MONTHLY, forward_data)


def red_panda_flow():
    for data in rpk_consume(
        cfg.RED_PANDA_BROKER_0, [cfg.RED_PANDA_TOPIC], cfg.RED_PANDA_CONSUMER_GROUP
    ):

        @time_histogram(MONTHLY_FORWARD_TIME)
        def consume():
            model = parse_data_rpk(data.value)
            if model:
                save_to_db(model)

                # End point for metrics
                current_time_micros = time.time_ns()
                FINAL_DELAY.labels(
                    country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
                ).set(current_time_micros)

        consume()


def orchestrator_flow():
    @async_time_histogram(MONTHLY_FORWARD_TIME)
    async def server(websocket, path):
        data: bytes = await websocket.recv()
        model = parse_data(data)
        save_to_db(model)

        # End point for metrics
        current_time_micros = time.time_ns()
        FINAL_DELAY.labels(
            country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
        ).set(current_time_micros)

    start_server = websockets.serve(server, '0.0.0.0', cfg.WSS_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def serialised_orchestrator_flow():
    @async_time_histogram(MONTHLY_FORWARD_TIME)
    async def server(websocket, path):
        data: bytes = await websocket.recv()
        model = parse_data(data)
        save_to_db(model)

        # End point for metrics
        current_time_micros = time.time_ns()
        FINAL_DELAY.labels(
            country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
        ).set(current_time_micros)

    start_server = websockets.serve(server, '0.0.0.0', cfg.WSS_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def async_orchestrator_flow():
    @async_time_histogram(MONTHLY_FORWARD_TIME)
    async def server(websocket, path):
        data: bytes = await websocket.recv()
        model = parse_data_rpk(data)
        save_to_db(model)

        # End point for metrics
        current_time_micros = time.time_ns()
        FINAL_DELAY.labels(
            country=model[0]['city'], date=model[0]['date'].strftime('%Y-%m-%d')
        ).set(current_time_micros)

    start_server = websockets.serve(server, '0.0.0.0', cfg.WSS_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def run():
    if cfg.ARCHITECTURE == ARCHITECTURE_RMQ:
        rmq_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_ORCHESTRATOR:
        orchestrator_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_SERIALISED_ORCHESTRATOR:
        serialised_orchestrator_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_ASYNC_ORCHESTRATOR:
        async_orchestrator_flow()
    elif cfg.ARCHITECTURE == ARCHITECTURE_REDPANDA:
        red_panda_flow()
    else:
        raise ModuleNotFoundError
