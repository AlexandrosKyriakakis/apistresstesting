import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from config.config import Env
from config.logger import logger

app = FastAPI()
cfg = Env()


class Item(BaseModel):
    name: str
    price: str


@app.get('/')
async def get_example():
    response = requests.get(cfg.EXTERNAL_HOST)
    logger.info('consumed response from external source: %s', str(response.content))
    return {'status_code': response.status_code, 'content': response.content}


@app.post('/')
async def get_example(item: Item):
    logger.info('consumed response from external source: %s, %s', item.name, item.price)
    return {'message': 'Item created successfully'}


if __name__ == '__main__':
    uvicorn.run(
        'src.rest.api:app', host='0.0.0.0', port=8000, log_level='info', workers=5
    )
