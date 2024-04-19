import fastapi_jsonrpc as jsonrpc
from src_mirror_back.app.api.rest.routers import add_rest_routers


def init_routers(app: jsonrpc.API) -> None:
    add_rest_routers(app)
