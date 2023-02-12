"""This module contains the serve function."""
import logging

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
    try:
        response = str(requests.get('http://127.0.0.1:8000').content)
    except requests.exceptions.ConnectionError:
        logger.info('Got Nothing')
    print('started', response)
    return True
