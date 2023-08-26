from telebot.handler_backends import State, StatesGroup


class CardState(StatesGroup):
    card = State()


class RegisterUserStates(StatesGroup):
    """ states for registratons """
    f_name = State()
    l_name = State()
    phone_number = State()
    birth_day = State()
    submit = State()