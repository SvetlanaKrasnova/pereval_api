import atexit
import logging
import queue
from contextlib import asynccontextmanager
from logging.handlers import QueueListener
from typing import AsyncContextManager

from fastapi import FastAPI

from src.api import api_router
from src.core.logger import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('pereval')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    queue_listener = QueueListener(queue.Queue(), logging.FileHandler('../logs/pereval.log'))
    try:
        queue_listener.start()
        atexit.register(queue_listener.stop)
        yield
    finally:
        logger.exception('ERROR - Application is shutting down.')
        queue_listener.stop()


app = FastAPI(lifespan=lifespan, docs_url='/api/openapi')
app.include_router(api_router)
