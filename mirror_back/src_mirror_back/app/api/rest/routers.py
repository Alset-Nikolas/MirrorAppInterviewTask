"""Route creator for w_mount service."""

import fastapi_jsonrpc as jsonrpc
from fastapi import APIRouter, Depends
from fastapi_jsonapi import RoutersJSONAPI
from fastapi_jsonapi.data_layers.orm import DBORMType

from src_mirror_back.app.api.rest.schemas.requests.order import OrderCreateSchema, OrderUpdateSchema
from src_mirror_back.app.api.rest.views.health import router as router_health
from src_mirror_back.app.api.rest.views.order import OrderDetail, OrderList
from src_mirror_back.app.db.orm import Order
from src_mirror_back.app.db.schemas import OrderSchema


def get_session():
    return True


def is_database_online(session: bool = Depends(get_session)):
    return session


def add_rest_routers(app: jsonrpc.API) -> None:
    routers: APIRouter = APIRouter()
    RoutersJSONAPI(
        routers=routers,
        path='/api/mirror-back/orders',
        tags=['Order'],
        class_detail=OrderDetail,
        class_list=OrderList,
        schema=OrderSchema,
        type_resource='orders',
        schema_in_patch=OrderUpdateSchema,
        schema_in_post=OrderCreateSchema,
        model=Order,
        engine=DBORMType.sqlalchemy,
    )
    app.include_router(router_health, prefix='')
    app.include_router(routers, prefix='')
