from telebot.handler_backends import State, StatesGroup

class RegisterUserState(StatesGroup):
    f_name = State()
    l_name = State()
    username = State()
    save = State()
    

class ProductStates(StatesGroup):
    title = State()
    description = State()
    category_id = State()



class ProductSizeState(StatesGroup):
    size = State()
    price = State()
    count = State()
    save = State()



class ProductColorState(StatesGroup):
    color = State()
    image = State()
    price = State()
    count = State()
    save = State()
