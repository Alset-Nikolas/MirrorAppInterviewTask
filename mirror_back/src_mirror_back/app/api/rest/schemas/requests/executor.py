from typing import Optional

from pydantic import BaseModel
from src_mirror_back.app.utils.pydantic import IdUpdateSchemaMixin


class ExecutorCreateSchema(BaseModel):
	username: str


class ExecutorUpdateSchema(IdUpdateSchemaMixin):
	username: Optional[str] = None
