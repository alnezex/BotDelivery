from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F
from contexts import *
from repository import PostgresRepository
from utils import Delivery


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
        prid = db.find_product_id(data['product_name'])
        db.add_product_to_backet(usid, prid, data['product_amount'])
        await message.answer(text=f'Отлично ты выбрал заказать {data['product_name']}, в количестве {data['product_amount']} шт. Я добавил это в твою корзину.\nЧтобы посмотреть свою корзину напиши /backet')
        await state.clear()

    else:
        await message.answer(text=f"Сорри, '{message.text}' - это не число, попробуй еще раз : ( или напиши stop чтобы прекрать добавление нового заказа")
        await state.set_state(Order.product_amount)



@rt_state.message(CustOrders.id)
async def custorders1(message: Message, db: PostgresRepository, state: FSMContext):
    if message.text == 'stop':
        await state.clear()
    elif not message.text.isdigit():
        await message.answer('ID состоит только из цифр, ты что-то путаешь')
        await state.set_state(CustOrders.id)
    elif db.find_user_id(message.text):
        usid = message.text

        totalpr = 0
        if len(db.show_backet(usid)) != 0:
            for product_name, info in db.show_backet(usid).items():
                await message.answer(f'{product_name}, {info[1]} шт, {info[0]}р * {info[1]}шт={info[0]*info[1]}')
                totalpr += info[0]*info[1]
            await message.answer(f'Итого: {totalpr}р')
        else:
            await message.answer(f'Корзина пуста')

        await state.clear()
    else:
        await message.answer('Такого юзера у нас нет, чтобы отменить операцию напиши stop')
        await state.set_state(CustOrders.id)



@rt_state.message(Place.city_name)
async def city_name(message: Message, db: PostgresRepository, state: FSMContext):
    if message.text == 'stop':
        await message.answer("Операция оформения заказа завершена ")
        await state.clear()
    
    elif message.text in db.get_cities():
        delivery = Delivery(db)
        distance = delivery.dijkstra('Москва', message.text)
        if distance:
            await message.answer(f"Ваш заказ в пути, направляется в город {message.text}, будет через {delivery.dijkstra('Москва', message.text)}, также ваша корзина теперь пуста.\nМожете начать добавлять туда, что-нибудь новое")
            db.delete_backet(message.from_user.id)
        else:
            await message.answer(f'извините но мы до вас не доедем(, выберите другой город\nПусть заберет заказ ваш друг или напиши stop для отмены операции ')
            await state.set_state(Place.city_name)
    else:
        await message.answer('такого города в наших базах нет, выберите другой или проверьте правильность написания названия и попробуйте еще раз или напиши stop для отмены операции')
        await state.set_state(Place.city_name)