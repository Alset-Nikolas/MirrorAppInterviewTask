from typing import Any, Dict

from src_mirror_back.app.db.creators.meta_base import BaseFactory
from src_mirror_back.app.db.orm import Executor


class ExecutorCreator(BaseFactory[Executor]):
    """Фабрика User."""

    class Meta:
        model = Executor

    data_fake = {}

    async def create(self) -> Executor:
        return await self._create()

    async def before_create(
        self,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        data_for_create: Dict[str, Any] = {}
        self.default_setter('username', input_data=kwargs, new_instance_as_dict=data_for_create)
        return data_for_create
