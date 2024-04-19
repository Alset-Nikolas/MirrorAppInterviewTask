from typing import Optional

from pydantic import BaseModel


class IdSchemaMixin(BaseModel):
    id: int


class IdUpdateSchemaMixin(BaseModel):
    id: Optional[int] = None
