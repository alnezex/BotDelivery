from aiogram.fsm.state import State, StatesGroup




class Order(StatesGroup):
    product_name = State()
    product_amount = State()


class CustOrders(StatesGroup):
    id = State()


class Place(StatesGroup):
    city_name = State()