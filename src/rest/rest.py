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

            response = str(
                requests.post(
                    cfg.API_SERVER_HOST, json={'name': 'alex', 'price': '3'}
                ).content
            )
            logger.info('consume api response %s', response)

            time.sleep(1)
        except requests.exceptions.ConnectionError:
            logger.error('got nothing')


if __name__ == '__main__':
    rest()
