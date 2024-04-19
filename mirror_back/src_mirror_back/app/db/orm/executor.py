from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Column

from src_mirror_back.app.extensions.sqlalchemy import Base
from src_mirror_back.app.utils.sqlalchemy import BaseModelMixin
from src_mirror_back.app.utils.sqlalchemy.association_column import association_relationship

if TYPE_CHECKING:
	from src_mirror_back.app.db.orm import Order


class Executor(Base, BaseModelMixin):
	__tablename__ = 'executors'
	__mapper_args__ = {'eager_defaults': True}

	id: int = Column(BigInteger, primary_key=True)
	username = Column(String)

	orders: list['Order'] = association_relationship(
		'Order',
		back_populates='executor',
		foreign_keys='Order.executor_id',
	)

	def __repr__(self):
		return '<Executor ID={id} username={username}>'.format(
			id=self.id,
			username=self.username,
		)
