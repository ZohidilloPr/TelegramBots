from telebot.handler_backends import State, StatesGroup


class TranslaterState(StatesGroup):
    word = State()

class WikipideaState(StatesGroup):
    word = State()