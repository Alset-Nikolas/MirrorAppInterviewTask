import datetime

from fastapi import Depends, HTTPException, status
from fastapi_jsonapi import QueryStringManager
from fastapi_jsonapi.schema import JSONAPIResultListSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src_mirror_back.app.api.rest.schemas.requests import OrderCreateSchema
from src_mirror_back.app.db.creators import (ErrorCreateObject,
                                             ErrorUniqObjectExist,
                                             FactoryUseMode, OrderCreator)
from src_mirror_back.app.db.orm import Order
from src_mirror_back.app.db.schemas import OrderSchema
from src_mirror_back.app.extensions.sqlalchemy import PoolConnector


class OrderList:
	@classmethod
	async def get(
			cls,
			query_params: QueryStringManager,
			session: AsyncSession = Depends(PoolConnector.get_session),
	) -> JSONAPIResultListSchema:
		query = select(Order)
		for i_filter in query_params.filters:
			if 'date' == i_filter['name']:
				date_ = datetime.datetime.strptime(i_filter['val'], "%Y-%m-%d")
				query = query.filter(Order.date == date_)
		query = query.order_by(Order.id)

		result = (await session.execute(query)).scalars().all()

		instances: list[OrderSchema] = [OrderSchema.from_orm(i_user) for i_user in result]

		return JSONAPIResultListSchema(
			meta={'count': len(instances), 'totalPages': 1},
			data=[{'id': i_obj.id, 'attributes': i_obj.dict(), 'type': 'orders'} for i_obj in instances],
		)

	@classmethod
	async def post(
			cls,
			data: OrderCreateSchema,
			session: AsyncSession = Depends(PoolConnector.get_session),
	) -> OrderSchema:
		try:
			instance: Order = await OrderCreator(
				**data.dict(),
				session=session,
				mode=FactoryUseMode.production,
			).create()
		except ErrorUniqObjectExist as err:
			return OrderSchema.from_orm(err.obj)
		except ErrorCreateObject as ex:
			raise HTTPException(
				detail=ex.description,
				status_code=status.HTTP_400_BAD_REQUEST,
			)
		return OrderSchema.from_orm(instance)


class OrderDetail:
	pass
