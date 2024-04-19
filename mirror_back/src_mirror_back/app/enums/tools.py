from src_mirror_back.app.utils.sqlalchemy.fields.enum import Enum


class HealthStatusType(str, Enum):
    ok = 'ok'
    error = 'error'
