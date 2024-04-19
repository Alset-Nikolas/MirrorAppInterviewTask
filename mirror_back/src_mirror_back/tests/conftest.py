import asyncio
import logging
import os
import threading
from pkgutil import walk_packages
from typing import TypeVar, Union

import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

from src_mirror_back import tests
from src_mirror_back.app.config import settings
from src_mirror_back.app.extensions.logging import logger
from src_mirror_back.app.extensions.sqlalchemy import Base, init_pool

thread_storage = threading.local()
TypeBaseModel = TypeVar('TypeBaseModel', bound=Base)

module = tests.fixtures
pytest_plugins = [
	*[
		package.name
		for package in walk_packages(
			path=module.__path__,
			prefix=module.__name__ + '.',
		)
	],
]


@pytest.yield_fixture(scope='session')
def event_loop():
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.yield_fixture(scope='session', autouse=True)
async def session(event_loop) -> AsyncSession:
	"""Создаём сессию"""
	assert settings.POSTGRES_DB.endswith('_test')
	pool = init_pool.create_pool()
	print('CREATE SESSION')
	async with pool() as session:
		yield session


async def deleted(session: AsyncSession, models: Union[list[TypeBaseModel], TypeBaseModel]):
	models = models if isinstance(models, (list, tuple)) else [models]
	for i_model in models:
		try:
			await i_model.delete(session=session)
		except Exception as ex:
			logger.error(ex)
			await session.rollback()
	await session.commit()


def recreate_db():
	uri = 'postgresql://{login}:{password}@{host}:{port}/{db}'.format(
		login=settings.POSTGRES_USER,
		password=settings.POSTGRES_PASSWORD,
		host=settings.POSTGRES_HOST,
		port=settings.POSTGRES_PORT,
		db=settings.POSTGRES_DB,
	)
	logger.debug('Recreate DB..')
	engine = create_engine(uri)
	if database_exists(engine.url):
		drop_database(engine.url)
	create_database(engine.url)
	logger.debug('Recreated DB')


def run_migrations() -> None:
	logger.debug('Running migrations')
	uri = 'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db}'.format(
		login=settings.POSTGRES_USER,
		password=settings.POSTGRES_PASSWORD,
		host=settings.POSTGRES_HOST,
		port=settings.POSTGRES_PORT,
		db=settings.POSTGRES_DB,
	)
	logging.info(uri)
	logging.disable(logging.INFO)
	_tests_folder_path = os.path.dirname(os.path.abspath(__file__))
	_app_folder_path = os.path.dirname(_tests_folder_path)
	migrations_folder_path = os.path.join(_app_folder_path, 'migrations')

	alembic_cfg = Config(file_=os.path.join(_app_folder_path, 'alembic.ini'))

	alembic_cfg.set_main_option('script_location', migrations_folder_path)
	alembic_cfg.set_main_option('sqlalchemy.url', uri)
	upgrade(alembic_cfg, 'head')
	logging.disable(logging.NOTSET)


def setup_database():
	logger.debug('Setup database')
	recreate_db()
	run_migrations()


def pytest_configure():
	logging.disable(logging.INFO)
	logging.disable(logging.WARN)
	logging.disable(logging.NOTSET)
	logger.debug('Initing pytest')

	setup_database()

	logger.debug('Done configuring pytest')

