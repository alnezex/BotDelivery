from aiogram.filters import BaseFilter
from aiogram.types import Message
from repository import PostgresRepository


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, db: PostgresRepository):
            return message.from_user.id in db.get_admins_tgid()


