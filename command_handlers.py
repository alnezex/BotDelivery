from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from contexts import Order
from aiogram.fsm.context import FSMContext
from repository import PostgresRepository

rt_cmd = Router()



@rt_cmd.message(CommandStart())
async def start(message: Message, db):
    if not db.is_registrated(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer(text=f"Привет, {message.from_user.full_name}!\nЯ бот для обработки заказов :)")


@rt_cmd.message(Command("order"))
async def order(message: Message, state: FSMContext):
    await state.set_state(Order.product_name)
    await message.answer(text="Напиши товары которые нужно заказать")

    
@rt_cmd.message(Command('admin'))
async def admin(message: Message, db: PostgresRepository):
    if db.is_admin(message.from_user.id):
        ...
    else:
        await message.answer(text='досвидания, больше не возвращайся')

@rt_cmd.message(Command('backet'))
async def backet(message: Message, db: PostgresRepository):
    usid = db.find_user_id(message.from_user.id)
    await message.answer('Вот ваша корзина, с товароми, чтобы ее оформить напишите /place')
    for product in db.show_backet(usid):
        await message.answer(f'{product}')
        