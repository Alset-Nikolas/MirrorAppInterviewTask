import datetime
from typing import Optional

from pydantic import BaseModel
from src_mirror_back.app.utils.pydantic import IdUpdateSchemaMixin


class OrderCreateSchema(BaseModel):
	number_apartment: int
	nickname: str
	breed_name: str
	start_time: datetime.datetime
	end_time: datetime.datetime
	executor_id: int


class OrderUpdateSchema(IdUpdateSchemaMixin):
	number_apartment: Optional[int] = None
	nickname: Optional[str] = None
	breed_name: str
	start_time: Optional[datetime.datetime] = None
	end_time: Optional[datetime.datetime] = None
	executor_id: Optional[int] = None
