from datetime import datetime
from typing import Optional, TypeVar

from sqlalchemy import Column, DateTime, delete, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from src_mirror_back.app.extensions.sqlalchemy import Base

TypeBase = TypeVar('TypeBase', bound=Base)
Model = TypeVar('Model', 'BaseModelMixin', 'BaseModelMixin')


class BaseModelMixin(object):
	id: int

	@declared_attr
	def created_at(self) -> Column[DateTime]:
		"""
		Дата создания записи.

		:return: Дата создания сущности.
		"""
		return Column('created_at', DateTime, default=datetime.utcnow)

	@declared_attr
	def modified_at(self) -> Column[DateTime]:
		"""
		Дата изменения записи.

		:return: Дата изменения сущности.
		"""
		return Column('modified_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	def __repr__(self) -> str:
		return '<{class_name}, pk: {primary_keys}>'.format(
			class_name=self.__class__.__name__,
			primary_keys=', '.join(str(getattr(self, key.name)) for key in inspect(self.__class__).primary_key),
		)

	async def save(self, session: AsyncSession, commit: bool = True, flush: bool = False) -> Model:
		has_pk: bool = all(getattr(self, key.name) for key in inspect(self.__class__).primary_key)
		if has_pk:
			await session.merge(self)
		else:
			session.add(self)
		if commit:
			await session.commit()
		elif flush:
			await session.flush()
		return self

	async def delete(self, session: AsyncSession, commit: bool = True) -> Optional[Model]:
		await session.execute(delete(self.__class__).where(self.__class__.id == self.id))
		if commit:
			await session.commit()
			return None
		return self

	@classmethod
	async def get_all(cls, session: AsyncSession) -> list[Model]:
		query = await session.execute(select(cls))
		return query.scalars().all()

	@classmethod
	async def get_by_id(cls, id_: int, session: AsyncSession) -> Model:
		query = await session.execute(select(cls).where(cls.id == id_))
		return query.scalar_one()

	@classmethod
	async def get_or_none(cls, id_: int, session: AsyncSession) -> Optional[Model]:
		query = await session.execute(select(cls).where(cls.id == id_))
		return query.scalar_one_or_none()
