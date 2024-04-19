import inspect
from enum import Enum
from typing import Any, Callable, Coroutine, Dict, Generic, Optional, Type, TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession
from src_mirror_back.app.extensions.sqlalchemy import Base

TypeBaseModel = TypeVar('TypeBaseModel', bound=Base)
FuncFake = Callable[
    [AsyncSession],
    Union[
        Coroutine[Any, Any, Any],
        Any,
    ],
]


class FactoryUseMode(Enum):
    test = 1  # для тестов, то есть данные генерируются случайно (если не заданы они явно)
    production = 2  # рабочий вариант, нельзя допустить случайную генерацию данных


class ExceptionBreak(Exception):
    """Исключения для прерывания создания объекта."""

    instance: Optional[TypeBaseModel]  # type: ignore

    def __init__(self, *args: Union[Any], **kwargs: Union[Any]) -> None:
        super().__init__(*args)
        self.instance = kwargs.get('instance')


class BaseFactory(Generic[TypeBaseModel]):
    class Meta:
        model = Type[TypeBaseModel]

    data_fake: Dict[str, FuncFake] = {}

    def __init__(
        self,
        session: AsyncSession,
        *args: Any,
        commit_model: bool = True,
        mode: FactoryUseMode = FactoryUseMode.test,
        **kwargs: Any,
    ) -> None:
        """
        Задаём действие для метода __init__ в фабриках.

        :param args: дополнительные аргументы.
        :param commit_model: при создание объекта, commit его
                             или просто сделать flush.
        :param session: сессия в рамках которой работаем.
        :param mode: для чего используется фабрика.
        :param kwargs: именованные параметры для фабрики.
        """
        self.args = args
        self.commit_model = commit_model
        self.session = session
        self.mode = mode
        self.kwargs = kwargs

    async def create(self) -> TypeBaseModel:
        """
        Создание сущности.

        В фабрики необходимо переопределить тип и выставить
         корректную аннотацию возвращаемому результату. В тело
         метода нужно поместить вызов self._create(), чтобы объект создался.

        :return: созданная сущность.
        """
        return await self._create()

    async def before_create(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Выполняет логику до начала работы фабрики.

        :param kwargs: параметры переданные для создания сущности.
        :return: именованные параметры для создания объекта.
        """
        return kwargs

    async def before_commit(self, result_data: TypeBaseModel) -> None:
        """
        Выполняет логику после создания объекта, но до commit в БД.

        :param result_data: очищенные данные для создания сущности.
        """

    async def after_commit(
        self,
        result_data: TypeBaseModel,
        commit_model: bool = False,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Выполняет логику после commit данных.

        :param result_data: созданная сущность.
        :param commit_model: нужно ли сохранять изменения?
        :param kwargs: сырые данные.
        """

    async def _commit(self, result_data: TypeBaseModel) -> None:
        if self.commit_model:
            await self.session.commit()

        await self.after_commit(result_data, kwargs=self.kwargs)

        if self.commit_model:
            await self.session.commit()

    async def _update_new_kwargs_for_fixture(self, new_kwargs: Dict[str, Any]) -> None:
        """
        Создание фейковых данных.

        Если у нас фабрика запущена в тестовом режиме и которые пользователь
         не прислал какие-то данные, то мы их дополняем фейковыми.

        :param new_kwargs: сырые данные для создания сущности.
        """
        for name, func_fake in self.data_fake.items():
            if name not in new_kwargs:
                if inspect.iscoroutinefunction(func_fake):
                    new_kwargs[name] = await func_fake(self.session)
                else:
                    new_kwargs[name] = func_fake(self.session)

    async def _create(self) -> Union[Any, 'TypeBaseFactory']:
        session = self.session

        new_kwargs = {}
        new_kwargs.update(self.kwargs)
        if self.mode is FactoryUseMode.test:
            await self._update_new_kwargs_for_fixture(new_kwargs)

        try:
            new_kwargs = await self.before_create(**new_kwargs)
        except ExceptionBreak as ex_before_create:
            return ex_before_create.instance
        # Удаляем поля, которых нет в модели
        # "object" has no attribute "__table__"- очень странно, описал
        # как Type[..], но всё равно считает что там object
        columns_model = self.Meta.model.__table__.columns  # type: ignore
        for i_key in set(new_kwargs.keys()) - set(columns_model.keys()):
            new_kwargs.pop(i_key, None)
        # "object" not callable- очень странно, описал как Type[..],
        # но всё равно считает что там object
        new_object = self.Meta.model(**new_kwargs)  # type: ignore
        await new_object.save(session=session, commit=False)
        result_data = new_object

        try:
            await self.before_commit(result_data)
        except ExceptionBreak as ex_before_commit:
            return ex_before_commit.instance
        try:
            await self._commit(result_data)
        except ExceptionBreak as ex_commit:
            return ex_commit.instance

        return result_data

    @classmethod
    def default_setter(cls, attribute_name: str, input_data: Dict, new_instance_as_dict: Dict):
        name_field: str = attribute_name
        value = input_data.get(name_field)
        new_instance_as_dict[name_field] = value


# Missing type parameters for generic type "BaseFactory"
TypeBaseFactory = TypeVar('TypeBaseFactory', bound=BaseFactory)  # type: ignore


def factory_import(name: str) -> Type[TypeBaseFactory]:
    components = name.split('.')
    mod = __import__('.'.join(components[:-1]))  # noqa: WPS421
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod  # type: ignore


async def create_from_factory(factory: str, **kwargs: Union[Any]) -> TypeBaseModel:
    factory_clss: Type[BaseFactory[TypeBaseModel]] = factory_import(factory)
    return await factory_clss(**kwargs).create()


async def create_model(session: AsyncSession, factory: str) -> int:
    model: TypeBaseModel = await create_from_factory(factory, session=session)
    return model.id
