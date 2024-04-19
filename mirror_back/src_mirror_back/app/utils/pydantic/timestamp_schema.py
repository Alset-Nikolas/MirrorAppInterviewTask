import datetime
from typing import Optional

from pydantic import BaseModel


class TimestampSchemaMixin(BaseModel):
    created_at: Optional[datetime.datetime] = None
    modified_at: Optional[datetime.datetime] = None
