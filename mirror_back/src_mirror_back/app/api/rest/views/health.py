from fastapi import APIRouter

from src_mirror_back.app.api.rest.schemas.responses.health import HealthSchema
from src_mirror_back.app.enums import HealthStatusType
from src_mirror_back.app.extensions.logging import logger
from src_mirror_back.app.extensions.sqlalchemy import PoolConnector

router = APIRouter(tags=['tools'])


class HealthController(object):
    @classmethod
    async def _connect_sql(cls):
        pool_connector = PoolConnector()
        session = pool_connector.get_session()

    @classmethod
    async def _check_sql(cls, health: HealthSchema):
        try:
            await cls._connect_sql()
        except Exception as exc:  # noqa pylint: disable=W0703
            health.sql_status = HealthStatusType.error
            logger.error('sql health error {0}'.format(str(exc)))
        else:
            health.sql_status = HealthStatusType.ok

    @classmethod
    async def create(cls) -> HealthSchema:
        health = HealthSchema()
        await cls._check_sql(health)
        return health


@router.get('/api/gpt-back/health', response_model_exclude_none=True, response_model=HealthSchema)
async def health_check() -> HealthSchema:
    return await HealthController.create()
