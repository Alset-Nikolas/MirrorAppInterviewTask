from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, String
from src_mirror_back.app.extensions.sqlalchemy import Base
from src_mirror_back.app.utils.sqlalchemy import BaseModelMixin
from src_mirror_back.app.utils.sqlalchemy.association_column import (
    AssociationColumn, association_relationship)

if TYPE_CHECKING:
	from src_mirror_back.app.db.orm import Executor


class Order(Base, BaseModelMixin):
	__tablename__ = 'orders'
	__mapper_args__ = {'eager_defaults': True}

	id: int = Column(BigInteger, primary_key=True)
	number_apartment: int = Column(Integer)
	nickname: str = Column(String)
	breed_name: str = Column(String)
	date = Column(Date, index=True)
	start_time: datetime = Column(DateTime(timezone=True))
	end_time: datetime = Column(DateTime(timezone=True))
	executor_id: int = AssociationColumn('executors.id')
	executor: 'Executor' = association_relationship(
		'Executor',
		foreign_keys=executor_id,
		back_populates='orders',
	)

	def __repr__(self):
		return '<Order ID={id} executor_id={executor_id} number_apartment={number_apartment} start_time: {start_time}>'.format(
			id=self.id,
			executor_id=self.executor_id,
			number_apartment=self.number_apartment,
			start_time=self.start_time,
		)
