import asyncio
import calendar
import datetime
import json
import sys
import time

import orjson as orjson
import pika as pika
import requests
import websockets
from kafka import KafkaProducer

from config.config import Env
from config.enum import ARCHITECTURE_ASYNC_ORCHESTRATOR
from config.enum import ARCHITECTURE_ORCHESTRATOR
from config.enum import ARCHITECTURE_REDPANDA
from config.enum import ARCHITECTURE_RMQ
from config.enum import ARCHITECTURE_SERIALISED_ORCHESTRATOR
from config.logger import logger
from src.postgres import Session
from src.postgres.models.my_model import TotalLoad
from src.prometheus.prometheus import DATA_REQUEST_TIME
from src.prometheus.prometheus import DATA_SAVE_TIME
from src.prometheus.prometheus import DATA_TOTAL_BYTES_RECEIVED
from src.prometheus.prometheus import DATA_TOTAL_REQUESTS_PROCESSED
from src.prometheus.prometheus import FINAL_DELAY
from src.prometheus.prometheus import time_histogram
from src.rmq.produce import produce as rmq_produce
from src.workers.data_worker.countries import COUNTRIES

cfg = Env()


@time_histogram(DATA_REQUEST_TIME)
def get_total_load(
    country: str, date: datetime.date, num_of_days: int = 1
) -> requests.Response:
    env = Env()

    url = (
        env.DATA_HOST + env.DATA_REQUEST + date.strftime('%Y/%m/%d/') + str(num_of_days)
    )
    payload = json.dumps({'areaRef': country + '_CTY_CTY', 'timezone': 'CET'})
    headers = {
        'x-auth-key': env.DATA_API_KEY,
        'Content-Type': 'application/json',
    }

    response = requests.request('GET', url, headers=headers, data=payload, json=orjson)

    # Total data processed
    DATA_TOTAL_BYTES_RECEIVED.inc(sys.getsizeof(response.content))
    DATA_TOTAL_REQUESTS_PROCESSED.inc()

    # Starting point for metrics TODO this is not working properly
    current_time_micros = time.time_ns()
    FINAL_DELAY.labels(
        country=country + '_CTY_CTY', date=date.strftime('%Y-%m-%d')
    ).set(current_time_micros)
    return response


def extract_load_data(response: requests.Response) -> bytes:
    # r_json = response.json()
    # return orjson.dumps(r_json['data']['TotalLoad'])
    return response.content


def get_next_date_num(date: datetime.date) -> tuple[datetime.date, int]:
    _, days_in_month = calendar.monthrange(date.year, date.month)
    days_left = days_in_month - date.day
    return date + datetime.timedelta(days=days_left + 1), days_left + 1


def pull_all_load_data():
    env = Env()

    # start_date = datetime.datetime.fromisoformat(env.DATA_START_DATE)
    start_date = datetime.datetime.fromisoformat(env.DATA_TEST_DATE)  # TODO REMOVE

    while start_date < datetime.datetime.today():
        next_date, num_of_days = get_next_date_num(start_date)
        if env.COUNTRY == '':
            for country in COUNTRIES.values():
                yield get_total_load(country, start_date, num_of_days).content
        else:
            yield get_total_load(env.COUNTRY, start_date, num_of_days).content

        start_date = next_date


@time_histogram(DATA_SAVE_TIME)
def save_to_db(body: bytes):
    data_batch = orjson.loads(body)
    session = Session()
    area_ref = data_batch['meta']['requestParams']['areaRefAbbrev']
    for d in data_batch['data']['TotalLoad']:
        session.add(
            TotalLoad(
                date_time=datetime.datetime.fromisoformat(d['DateTime'][:-1]),
                country=area_ref,
                load=int(d['value']),
            )
        )
    session.commit()
    session.close()


def rmq_flow():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RMQ_HOST))
    channel = connection.channel()

    for data in pull_all_load_data():
        rmq_produce(channel, cfg.RMQ_QUEUE_NAME_DAILY, data)
        save_to_db(data)


def red_panda_flow():
    producer = KafkaProducer(bootstrap_servers=cfg.RED_PANDA_BROKER_0)

    for data in pull_all_load_data():
        producer.send(cfg.RED_PANDA_TOPIC, key=cfg.RED_PANDA_KEY, value=data)
        save_to_db(data)
    producer.flush()
    producer.close()


def orchestrator_flow():
    for data in pull_all_load_data():

        async def client():
            async with websockets.connect(cfg.API_DAILY_HOST) as daily_websocket:
                await daily_websocket.send(data)
                daily_data: bytes = await daily_websocket.recv()
            async with websockets.connect(cfg.API_WEEKLY_HOST) as weekly_websocket:
                await weekly_websocket.send(daily_data)
                weekly_data: bytes = await weekly_websocket.recv()
            async with websockets.connect(cfg.API_MONTHLY_HOST) as monthly_websocket:
                await monthly_websocket.send(weekly_data)

        async def save():
            save_to_db(data)

        asyncio.get_event_loop().run_until_complete(asyncio.gather(client(), save()))


def serialised_orchestrator_flow():
    for data in pull_all_load_data():

        async def client():
            async with websockets.connect(cfg.API_DAILY_HOST) as daily_websocket:
                await daily_websocket.send(data)

        async def save():
            save_to_db(data)

        asyncio.get_event_loop().run_until_complete(asyncio.gather(client(), save()))


def async_orchestrator_flow():
    for data in pull_all_load_data():

        async def send_daily():
            async with websockets.connect(cfg.API_DAILY_HOST) as daily_websocket:
                await daily_websocket.send(data)

        async def send_weekly():
            async with websockets.connect(cfg.API_WEEKLY_HOST) as weekly_websocket:
                await weekly_websocket.send(data)

        async def send_monthly():
            async with websockets.connect(cfg.API_MONTHLY_HOST) as monthly_websocket:
                await monthly_websocket.send(data)

        async def save():
            save_to_db(data)

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(send_daily(), send_weekly(), send_monthly(), save())
        )


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

    logger.info('%s Just Ended', cfg.COUNTRY)
    while True:
        time.sleep(1)
