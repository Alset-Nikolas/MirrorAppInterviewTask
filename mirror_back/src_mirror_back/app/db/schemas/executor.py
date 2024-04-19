from src_mirror_back.app.utils.pydantic import OrmSchemaMixin


class ExecutorSchema(OrmSchemaMixin):
	id: int
	username: str
