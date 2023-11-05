import logging

from fastapi import FastAPI

from api_v1.routes.v1_router import v1_router

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info('Adding v1 endpoints...')

app.include_router(v1_router, prefix='/v1')

@app.on_event('startup')
async def startup():
    ...

@app.on_event('shutdown')
async def shutdown():
    ...




