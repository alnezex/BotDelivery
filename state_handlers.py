from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from contexts import Order
from repository import PostgresRepository

rt_state = Router()



@rt_state.message(Order.product_name)
async def get_orderprname(message: Message, state: FSMContext, db: PostgresRepository):
    if message.text == 'stop':
        await message.answer(text='добавление заказа завершенно')
        await state.clear()
        
    elif db.is_product_avaliable(message.text):
        await state.update_data(product_name=message.text, product_amount=None)
        await message.answer(text=f"Отлично, ты выбрал {message.text}, теперь напиши количество")
        await state.set_state(Order.product_amount)

    else:
        await message.answer(text=f"Сорри, но продукта '{message.text}' нет еще в моем магазине : (\nПопробуй еще раз, или напиши stop, чтобы прекратить добавление нового заказа")
        await state.set_state(Order.product_name)


@rt_state.message(Order.product_amount)
async def get_orderpramount(message: Message, state: FSMContext, db: PostgresRepository):
    if message.text == 'stop':
        await message.answer(text='добавление заказа завершенно')
        await state.clear()

    elif message.text.isdigit():
        await state.update_data(product_amount=message.text)
        data = await state.get_data()
        usid = db.find_user_id(message.from_user.id)
        db.add_product_to_backet(usid, data['product_name'], data['product_amount'])
        await message.answer(text=f'Отлично ты выбрал заказать {data['product_name']}, в количестве {data['product_amount']} шт. Я добавил это в твою корзину.\nЧтобы посмотреть свою корзину напиши /backet')
        await state.clear()

    else:
        await message.answer(text=f"Сорри, '{message.text}' - это не число, попробуй еще раз : ( или напиши stop чтобы прекрать добавление нового заказа")
        await state.set_state(Order.product_amount)