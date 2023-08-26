# --- Importing from libraries ---

from telebot.handler_backends import State, StatesGroup

''' Javob berish part of code '''
from enum import Enum

# --- The end of Importing from libraries ---


# --- Creating of class RegisterState(temporary storage) ---

class RegisterStates(StatesGroup):
    f_name = State()
    gender = State()
    birth_date = State()
    db_birth_date = State()
    number = State()
    city = State()
    street = State()
    submit = State()

# --- The end of Creating of class RegisterState(temporary storage) ---


# --- Creating of class MessageStates(temporary storage) ---

class MessageStates(StatesGroup):
    appeals_type = State()
    user_problem_type = State()
    user_message = State()
    document_id = State()
    yes_or_no = State()
    photo_id = State()
    video_id = State()
    submit = State()


class SeeAllAppeals(StatesGroup):
    user_id = State()
    to_excel = State()

# --- The end of Creating of class MessageStates(temporary storage) ---


# --- Creating of class AdminStates(temporary storage) ---

class AdminStates(StatesGroup):
    message = State()

# --- The end of Creating of class AdminStates(temporary storage) ---

class AddProblemType(StatesGroup):
    appeals_type = State()
    name = State()

class RemoveProblemType(StatesGroup):
    appeals_type = State()
    name = State()

