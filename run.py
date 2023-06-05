import os
import time

from prometheus_client import start_http_server

import config.enum as enum
from config.config import Env
from config.logger import logger
from src.postgres.init_db import init_db
from src.redpanda.pubsub import pubsub
from src.rest.rest import rest
from src.rmq.rmq import rmq
from src.workers.daily_worker import daily_worker
from src.workers.data_worker import data_worker
from src.workers.monthly_worker import monthly_worker
from src.workers.weekly_worker import weekly_worker

if __name__ == '__main__':
    cfg = Env()
    time.sleep(10)
    init_db()

    # Start up the server to expose the metrics.
    start_http_server(5000)

    if cfg.ROLE == enum.ROLE_DATA_WORKER:
        data_worker.run()
    elif cfg.ROLE == enum.ROLE_DAILY_WORKER:
        daily_worker.run()
    elif cfg.ROLE == enum.ROLE_WEEKLY_WORKER:
        weekly_worker.run()
    elif cfg.ROLE == enum.ROLE_MONTHLY_WORKER:
        monthly_worker.run()
    else:
        logger.error('wrong env variable ROLE: %s', os.getenv('ROLE'))

# Deprecated
# if cfg.ROLE in enum.red_panda_roles:
#     pubsub()
# elif cfg.ROLE in enum.api_roles:
#     rest()
# elif cfg.ROLE in enum.rmq_roles:
#     rmq()
# else:
#     logger.error('wrong env variable ROLE: %s', os.getenv('ROLE'))
