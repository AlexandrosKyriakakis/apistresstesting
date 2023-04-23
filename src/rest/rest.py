import time

import requests

from config.config import Env
from config.logger import logger


def rest():
    cfg = Env()
    logger.info('starting rest api consumer')
    while True:
        try:
            response = str(requests.get(cfg.API_SERVER_HOST).content)
            logger.info('consume api response %s', response)
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            logger.error('got nothing')
