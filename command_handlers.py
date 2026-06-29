from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from contexts import *
from aiogram.fsm.context import FSMContext
from repository import PostgresRepository
from filters import AdminFilter



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

    
@rt_cmd.message(Command('admin'), AdminFilter())
async def admin(message: Message, db: PostgresRepository):
    await message.answer(text="Здравствуйте, дорогой admin.\nВот команды которые ты в праве использовать :\n/users - команда которая выведет всех пользователей\n/admins - выведет всех админов\n/custorders - выведет все актуальные заказы отдельного человека ")

@rt_cmd.message(Command('backet'))
async def backet(message: Message, db: PostgresRepository):
    usid = db.find_user_id(message.from_user.id)
    if len(db.show_backet(usid)) != 0:
        await message.answer('Вот ваша корзина, с товароми, чтобы ее оформить напишите /place')
        totalpr = 0
        for product_name, info in db.show_backet(usid).items():
            await message.answer(f'{product_name}, {info[1]} шт, {info[0]}р * {info[1]}шт={info[0]*info[1]}')
            totalpr += info[0]*info[1]
        await message.answer(f'Итого: {totalpr}р')
    else:
        await message.answer('Корзина пуста')
        

@rt_cmd.message(Command('users'), AdminFilter())
async def users(message: Message, db: PostgresRepository, bot: Bot):
    for user in db.get_users():
        us_info = await bot.get_chat(user[1])

        await message.answer(f"Username: {us_info.username}, firstname: {us_info.first_name}, lastname {us_info.last_name}, дата регистрации: {user[2]}")
@rt_cmd.message(Command('admins'), AdminFilter())
async def admins(message: Message, db: PostgresRepository, bot: Bot):
    for admin in db.get_admins():
        info = db.get_user(admin)
        us_info = await bot.get_chat(info[1])

        await message.answer(f"Username: {us_info.username}, firstname: {us_info.first_name}, lastname {us_info.last_name}, дата регистрации: {info[2]}")



@rt_cmd.message(Command('custorders'), AdminFilter())
async def custorders(message: Message, db: PostgresRepository, state: FSMContext):
    
    await message.answer(text="Отлично, ты хочешь узнать корзину определенного покупателя\nТогда отправь TELEGRAM id мне этого юзера")
    await state.set_state(CustOrders.id)



@rt_cmd.message(Command('place'))
async def place(message: Message, db: PostgresRepository, state: FSMContext):
    usid = db.find_user_id(message.from_user.id)
    if len(db.show_backet(usid)) != 0:
        await state.set_state(Place.city_name)
        totalpr = 0
        for product_name, info in db.show_backet(usid).items():
            totalpr += info[0]*info[1]

        await message.answer(f"Ваша конечная цена корзины составляет {totalpr} р.\nЧтобы перейти к оплате напиши город куда доставлять заказ .")
    else:
        await message.answer("Сорри но у тебя еще пустая корзина добавь туда чето")