from src_mirror_back.app.utils.pydantic import IdSchemaMixin
from src_mirror_back.app.utils.pydantic.timestamp_schema import \
    TimestampSchemaMixin


class IdResponseSchemaMixin(IdSchemaMixin):
	type: str


class ListResponseSchemaMixin(IdSchemaMixin):
	pass


class DetailResponseSchemaMixin(IdSchemaMixin, TimestampSchemaMixin):
	pass
