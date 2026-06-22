import os
from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
from asyncio import run
from repository import PostgresRepository
from utils import get_admin_cmd


from command_handlers import rt_cmd
from text_handlers import rt_text
from state_handlers import rt_state
load_dotenv()

bot = Bot(token=os.getenv("token"))

dp = Dispatcher()

dbname = os.getenv('dbname')
dbhost = os.getenv('dbhost')
dbpassword = os.getenv('dbpassword')
database = PostgresRepository(dbname, dbhost, dbpassword)
dp['db'] = database



async def main():
    dp.include_routers(rt_cmd, rt_state, rt_text)
    await bot.set_my_commands([get_admin_cmd()])
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())