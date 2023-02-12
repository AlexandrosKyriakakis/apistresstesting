import requests
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def get_example():
    response = requests.get('http://example.com')
    print(response.content)
    return {'status_code': response.status_code, 'content': response.content}
