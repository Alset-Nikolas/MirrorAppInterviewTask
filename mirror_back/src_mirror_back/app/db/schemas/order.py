import datetime

from src_mirror_back.app.utils.pydantic import OrmSchemaMixin


class OrderSchema(OrmSchemaMixin):
	number_apartment: int
	nickname: str
	number_apartment: str
	date: datetime.date
	start_time: datetime.datetime
	end_time: datetime.datetime
	executor_id: int
