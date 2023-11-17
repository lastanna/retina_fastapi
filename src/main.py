import logging
import logging.config
import uvicorn

from fastapi import FastAPI

from src.api.v1.router import router as v1_router
from src.api.v1.events import router as events
from src.core.config import app_settings
from src.core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=app_settings.app_title,
)

app.include_router(v1_router, prefix='/api/v1')
app.include_router(events, prefix='/events')

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=app_settings.project_host,
        port=app_settings.project_port
    )

