from fastapi import FastAPI
from .routers import post_router

app = FastAPI(title='Social Network Posts', version='1')

app.include_router(post_router)

@app.get('/')
async def index():
    return 'Hello World, go to /docs to see the endpoints and make requests'