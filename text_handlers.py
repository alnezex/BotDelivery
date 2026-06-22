from aiogram.types import Message
from aiogram import F
from aiogram import Router


rt_text = Router()







@rt_text.message(F.text)
async def msg(message: Message):
    exact_message = message.text
    if len(exact_message.split(' ')) == 2 and type(exact_message.split(' ')[0]) == str and exact_message.split(' ')[1].isdigit():
        await message.answer(text='ты молодец, правильно все написал')
    else:
        await message.answer(text="Вы неправильно ввели сообщение")
