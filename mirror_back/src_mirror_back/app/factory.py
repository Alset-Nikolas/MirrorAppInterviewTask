import fastapi_jsonrpc as jsonrpc
import openai
import sentry_sdk
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src_mirror_back.app.api.urls import init_routers
from src_mirror_back.app.config import settings
from src_mirror_back.app.extensions.logging import logger
from src_mirror_back.app.extensions.sqlalchemy import PoolConnector, init_pool


def create_app() -> FastAPI:
    """
    Create app factory.

    :return: app
    """
    if settings.SENTRY_DSN:
        logger.info('Init sentry')
        sentry_sdk.init(dsn=settings.SENTRY_DSN)

    app = jsonrpc.API(
        title='Mirror Test Task',
        debug=settings.DEBUG,
        openapi_url='/api/mirror-back/openapi.json',
        docs_url='/api/mirror-back/docs',
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_routers(app)
    PoolConnector()
    return app
