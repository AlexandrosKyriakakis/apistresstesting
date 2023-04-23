import os
import time

from config.config import Env
import config.enum as enum
from config.logger import logger
from src.pubsub.pubsub import pubsub
from src.rest.rest import rest

if __name__ == '__main__':
    cfg = Env()
    if cfg.ROLE in enum.red_panda_roles:
        time.sleep(10)
        pubsub()
    elif cfg.ROLE in enum.api_roles:
        time.sleep(10)
        rest()
    else:
        logger.error('ERROR ENV VAR')
        logger.error('ROLE: %s', os.getenv('ROLE'))
