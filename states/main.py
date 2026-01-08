from aiogram.dispatcher.filters.state import State, StatesGroup


class AddProductFSM(StatesGroup):
    table = State()

class mainstate(StatesGroup):
    menu = State()


class process(StatesGroup):
    table = State()
    product = State()
    change_table = State()
    nakladnoy = State()
    number_nakladnoy = State()
    nakladnoy_price = State()
    nakladnoy_sell_price = State()
    
    
    

class delete_nakladnoy(StatesGroup):
    delete_nakladnoy_choose = State()
    choose_product = State()
    input_amount = State()
    delete = State()


class sell_product(StatesGroup):
    sell = State()



