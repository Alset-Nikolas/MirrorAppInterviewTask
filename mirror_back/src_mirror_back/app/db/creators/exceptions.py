from typing import Any, Type, TypeVar

from src_mirror_back.app.extensions.sqlalchemy import Base

TypeBase = TypeVar('TypeBase', bound=Base)


class ErrorCreateObject(Exception):
    def __init__(self, model: Type['TypeBase'], description: str, field_name: str = ''):
        self.model = model
        self.message = description
        self.field_name = field_name
        self.description = description
        super().__init__(self.message)


class ErrorUniqObjectExist(Exception):
    def __init__(self, model: Type['TypeBase'], obj: Any, description: str, field_name: str = ''):
        self.model = model
        self.message = description
        self.field_name = field_name
        self.description = description
        self.obj = obj
        if not isinstance(self.obj, self.model):
            raise TypeError('Err type {obj} is not type {model} '.format(obj=self.obj, mpdel=self.model))
        super().__init__(self.message)
