import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src_mirror_back.app.db.creators import OrderCreator
from src_mirror_back.app.db.orm import Order
from src_mirror_back.tests.conftest import deleted


@pytest.fixture
async def order(session: AsyncSession) -> Order:
	instance = await OrderCreator(session=session).create()
	yield instance
	await deleted(session, instance)
