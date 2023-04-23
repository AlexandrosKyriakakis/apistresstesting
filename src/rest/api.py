import requests
from fastapi import FastAPI

from config.config import Env
from config.logger import logger

app = FastAPI()
cfg = Env()


@app.get('/')
async def get_example():
    response = requests.get(cfg.EXTERNAL_HOST)
    logger.info('consumed response from external source: %s', str(response.content))
    return {'status_code': response.status_code, 'content': response.content}
