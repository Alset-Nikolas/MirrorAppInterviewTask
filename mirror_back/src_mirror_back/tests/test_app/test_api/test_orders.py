import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src_mirror_back.app.api.rest.schemas.requests import OrderCreateSchema
from src_mirror_back.app.api.rest.views.order import OrderList


class TestOrderList:
    tested_class = OrderList

    async def test_not_working_hours(self, session: AsyncSession):
        '''Самая ранняя прогулка может начинаться не ранее 7-ми утра, а самая поздняя не позднее 11-ти вечера.'''
        day = datetime.datetime.now()
        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname',
                    breed_name='test_breed_name',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=6, minute=30),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=7),
                    executor_id=1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'not working hours start 7:00 end 23:00'

        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname',
                    breed_name='test_breed_name',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=23, minute=30),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=0, minute=0)
                    + datetime.timedelta(days=1),
                    executor_id=1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'not working hours start 7:00 end 23:00'

    async def test_limit_time_walk(self, session: AsyncSession):
        '''Прогулка может длиться не более получаса'''
        day = datetime.datetime.now()
        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname',
                    breed_name='test_breed_name',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=7),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=8),
                    executor_id=1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'Max end_time-start_time = 30min'

    async def test_err_start_time_walk(self, session: AsyncSession):
        '''Прогулка может начинаться либо в начале часа, либо в половину'''
        day = datetime.datetime.now()
        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname',
                    breed_name='test_breed_name',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=7, minute=1),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=8),
                    executor_id=1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'start_time minute 0 or 30'

    async def test_not_correct_executor(self, session: AsyncSession):
        '''В заказе необходимо сохранять номер квартиры, кличку и породу животного, время и дату прогулки. (Оформление заказа)'''
        day = datetime.datetime.now()
        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname_new',
                    breed_name='test_breed_name_new',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=7, minute=0),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=7, minute=30),
                    executor_id=-1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'Executor id=-1 not exist'

    async def test_busy_executor(self, session: AsyncSession):
        '''Пётр и Антон каждый могут гулять одновременно только с одним животным.'''
        day = datetime.datetime.now()
        await self.tested_class.post(
            session=session,
            data=OrderCreateSchema(
                number_apartment=1,
                nickname='test_nickname_new',
                breed_name='test_breed_name_new',
                start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=0),
                end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=30),
                executor_id=1,
            ),
        )
        with pytest.raises(HTTPException) as err:
            await self.tested_class.post(
                session=session,
                data=OrderCreateSchema(
                    number_apartment=1,
                    nickname='test_nickname_new',
                    breed_name='test_breed_name_new',
                    start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=0),
                    end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=30),
                    executor_id=1,
                ),
            )
        assert err.value.status_code == 400
        assert err.value.detail == 'Executor id=1 busy'

        await self.tested_class.post(
            session=session,
            data=OrderCreateSchema(
                number_apartment=2,
                nickname='test_nickname_new',
                breed_name='test_breed_name_new',
                start_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=0),
                end_time=datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, minute=30),
                executor_id=2,
            ),
        )
