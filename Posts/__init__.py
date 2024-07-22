from fastapi import FastAPI
from .routers import post_router
from .database import database, Post, Like

app = FastAPI(title='Social Network Posts', version='1')

app.include_router(post_router)

@app.get('/')
async def index():
    return 'Hello World, go to /docs to see the endpoints and make requests'

@app.on_event('startup')
def startup():
    if database.is_closed():
        database.connect()
        print('Connecting to database...')
        
    database.create_tables([Post, Like])


@app.on_event('shutdown')
def shutdown():
    if not database.is_closed():
        database.close()
        print('Closing database...')