from typing import Optional

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src_mirror_back.app.config import settings

Base = declarative_base()


class InitPool:
	engine: AsyncEngine

	def __init__(self):
		self.uri = 'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db}'.format(
			login=settings.POSTGRES_USER,
			password=settings.POSTGRES_PASSWORD,
			host=settings.POSTGRES_HOST,
			port=settings.POSTGRES_PORT,
			db=settings.POSTGRES_DB,
		)

	def create_pool(self, pool_size: int = 10) -> sessionmaker:
		self.engine: AsyncEngine = create_async_engine(
			url=make_url(self.uri),
			# pool_size=pool_size,
			echo=settings.POSTGRES_ECHO,
			pool_size=3,  # минимальное количество соединений в пуле
			max_overflow=pool_size,  # максимальное количество соединений в пуле
			pool_pre_ping=True,
			# включить предварительный пинг соединений перед их использованием, чтобы проверить их жизнеспособность
		)
		pool = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
		return pool


init_pool = InitPool()
async_session = init_pool.create_pool()


class PoolConnector:
	_instance: Optional['PoolConnector'] = None

	def __new__(cls):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls)  # noqa: WPS609
		return cls._instance

	def __init__(self):
		self.async_session = init_pool.create_pool()

	@classmethod
	async def get_session(cls):
		"""
		Получение сессии к БД.

		:return:
		"""

		async with async_session() as session:
			try:
				yield session
				await session.commit()
			except Exception:
				await session.rollback()
				raise
			finally:
				await session.close()
