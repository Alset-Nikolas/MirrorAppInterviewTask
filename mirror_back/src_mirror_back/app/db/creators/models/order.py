import datetime
from typing import Any, Dict

from sqlalchemy import select

from src_mirror_back.app.db.creators import ErrorCreateObject
from src_mirror_back.app.db.creators.meta_base import BaseFactory
from src_mirror_back.app.db.orm import Order, Executor


class OrderCreator(BaseFactory[Order]):
	"""Фабрика User."""

	class Meta:
		model = Order

	data_fake = {}

	async def create(self) -> Order:
		return await self._create()

	async def before_create(
			self,
			**kwargs: Dict[str, Any],
	) -> Dict[str, Any]:
		data_for_create: Dict[str, Any] = {}
		self._set_start_time(kwargs=kwargs, data_for_create=data_for_create)
		self._set_end_time(kwargs=kwargs, data_for_create=data_for_create)
		await self._set_executor_id(kwargs=kwargs, data_for_create=data_for_create)
		self.default_setter('number_apartment', input_data=kwargs, new_instance_as_dict=data_for_create)
		self.default_setter('nickname', input_data=kwargs, new_instance_as_dict=data_for_create)
		self.default_setter('breed_name', input_data=kwargs, new_instance_as_dict=data_for_create)
		self.default_setter('start_time', input_data=kwargs, new_instance_as_dict=data_for_create)
		self.default_setter('end_time', input_data=kwargs, new_instance_as_dict=data_for_create)
		self._set_date(kwargs=kwargs, data_for_create=data_for_create)
		return data_for_create

	def _set_start_time(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
		name_field: str = 'start_time'
		value: datetime.datetime = kwargs.get(name_field)

		# Самая ранняя прогулка может начинаться не ранее 7-ми утра, а самая поздняя не позднее 11-ти вечера.
		if 7 > value.hour or value.hour > 23 or (value.hour == 23 and value.minute > 0):
			raise ErrorCreateObject(
				model=Executor,
				description='not working hours start 7:00 end 23:00',
				field_name=name_field,
			)
		# Прогулка может начинаться либо в начале часа, либо в половину (11:00,11:30,12:00,12:30…).
		if value.minute not in [0, 30]:
			raise ErrorCreateObject(
				model=Executor,
				description='start_time minute 0 or 30',
				field_name=name_field,
			)

		data_for_create[name_field] = value

	def _set_date(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
		name_field: str = 'date'

		start_time_name_field: str = 'start_time'
		start_time: datetime.datetime = kwargs.get(start_time_name_field)

		data_for_create[name_field] = start_time.date()

	def _set_end_time(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
		name_field: str = 'end_time'
		value: datetime.datetime = kwargs.get(name_field)

		start_time_name_field: str = 'start_time'
		start_time: datetime.datetime = kwargs.get(start_time_name_field)
		if start_time >= value:
			raise ErrorCreateObject(
				model=Executor,
				description='start_time < end_time',
				field_name=name_field,
			)
		# 2. Прогулка может длиться не более получаса.
		if value - start_time > datetime.timedelta(minutes=30):
			raise ErrorCreateObject(
				model=Executor,
				description='Max end_time-start_time = 30min',
				field_name=name_field,
			)
		data_for_create[name_field] = value

	async def _set_executor_id(self, kwargs: Dict[str, Any], data_for_create: Dict[str, Any]) -> None:
		name_field: str = 'executor_id'
		value = kwargs.get(name_field)

		if not (await Executor.get_or_none(id_=value, session=self.session)):
			raise ErrorCreateObject(
				model=Executor,
				description='Executor id={id} not exist'.format(id=value),
				field_name=name_field,
			)
		name_field_start_time: str = 'start_time'
		start_time = kwargs.get(name_field_start_time)

		# Пётр и Антон каждый могут гулять одновременно только с одним животным.
		query = await self.session.execute(
			select(Order)
			.join(
				Executor,
				Order.executor_id == Executor.id,
			)
			.where(
				Executor.id == value,
				Order.start_time == start_time,
			),
		)
		result = query.scalar_one_or_none()
		if result:
			raise ErrorCreateObject(
				model=Executor,
				description='Executor id={id} busy'.format(id=value),
				field_name=name_field,
			)

		data_for_create[name_field] = value
# [{"name":"start_time","op":"ge","val":"2024-04-19T00:00:00.000000"}]
