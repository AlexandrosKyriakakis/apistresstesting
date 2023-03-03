"""This module contains the serve function."""
import logging
import time

import requests

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('api-stress-testing')


def serve() -> bool:
    """
    This function starts the program by printing 'started'.
    This function provides a simple starting point for the program
    by printing the string 'started'.
    """
    response = ''
    while True:
        try:
            time.sleep(1)
            response = str(requests.get('http://my_alias_c:8000').content)
            print('started', response)
        except requests.exceptions.ConnectionError:
            logger.info('Got Nothing')
    return True
