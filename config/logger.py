import logging


logging.basicConfig(
    format='%(pathname)s:%(lineno)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level='INFO',
)
logger = logging.getLogger('api-stress-testing')
