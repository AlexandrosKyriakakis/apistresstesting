import os
import time

from config.config import Env
import config.enum as enum
from config.logger import logger
from src.redpanda.pubsub import pubsub
from src.rest.rest import rest
from src.rmq.rmq import rmq
from src.postgres.init_db import init_db

if __name__ == '__main__':
    cfg = Env()
    time.sleep(10)
    init_db()
    if cfg.ROLE in enum.red_panda_roles:
        pubsub()
    elif cfg.ROLE in enum.api_roles:
        rest()
    elif cfg.ROLE in enum.rmq_roles:
        rmq()
    else:
        logger.error('wrong env variable ROLE: %s', os.getenv('ROLE'))
