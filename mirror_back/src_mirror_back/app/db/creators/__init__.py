from src_mirror_back.app.db.creators.exceptions import ErrorCreateObject, ErrorUniqObjectExist
from src_mirror_back.app.db.creators.faker import fake
from src_mirror_back.app.db.creators.meta_base import FactoryUseMode

FP: str = 'src_gpt_back.app.db.creators.'
# Перечисляем абсолютные пути до фабрик для избежания циклического импорта
user_creator: str = FP + 'ExecutorCreator'
order_creator: str = FP + 'OrderCreator'


from src_mirror_back.app.db.creators.models.executor import ExecutorCreator
from src_mirror_back.app.db.creators.models.order import OrderCreator
