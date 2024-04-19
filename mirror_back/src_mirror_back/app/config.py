import logging
import os
from typing import Optional, Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base settings."""

    # app
    DEBUG: bool
    RELOAD: bool
    NAME: str = 'mirror-back'
    LOG_LEVEL: int = logging.WARNING
    USE_JSON_LOG_FORMAT: bool = False

    CORS_ORIGINS: list = [
        '*',
    ]

    # sentry
    SENTRY_DSN: str = ''

    # postgres
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'qwerty'
    POSTGRES_DB: str = 'mirror_back'
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False

    class Config:
        env_file_encoding = 'utf-8'


class LocalSettings(Settings):
    DEBUG: bool = True
    RELOAD: bool = True

    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_PORT: int = 5432

    SENTRY_DSN: Optional[str] = None


class DockerSettings(Settings):
    DEBUG: bool = False
    RELOAD: bool = False

    POSTGRES_HOST: str = 'mirror_postgres'
    POSTGRES_PORT: int = 5432


class TestSettings(LocalSettings):
    POSTGRES_DB: str = 'mirror_back_test'


def get_settings() -> Union[DockerSettings, LocalSettings]:
    env_type = os.environ['TYPE_ENV']
    config_cls_dict = {'docker': DockerSettings, 'local': LocalSettings, 'test': TestSettings}
    config_cls = config_cls_dict[env_type]
    return config_cls()


settings = get_settings()
