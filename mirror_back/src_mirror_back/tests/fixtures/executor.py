import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src_mirror_back.app.db.creators import ExecutorCreator
from src_mirror_back.app.db.orm import Executor
from src_mirror_back.tests.conftest import deleted


@pytest.fixture
async def executor(session: AsyncSession) -> Executor:
	instance = await ExecutorCreator(session=session).create()
	yield instance
	await deleted(session, instance)
