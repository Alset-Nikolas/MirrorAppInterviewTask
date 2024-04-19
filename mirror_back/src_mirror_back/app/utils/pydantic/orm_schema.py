from src_mirror_back.app.utils.pydantic import IdSchemaMixin
from src_mirror_back.app.utils.pydantic.timestamp_schema import \
    TimestampSchemaMixin


class OrmSchemaMixin(IdSchemaMixin, TimestampSchemaMixin):
	class Config:
		orm_mode = True
		arbitrary_types_allowed = True
