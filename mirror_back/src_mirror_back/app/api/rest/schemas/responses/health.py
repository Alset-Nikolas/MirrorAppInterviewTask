from typing import Optional

from pydantic import BaseModel

from src_mirror_back.app.enums import HealthStatusType


class HealthSchema(BaseModel):
    status: HealthStatusType = HealthStatusType.ok
    sql_status: Optional[HealthStatusType]
