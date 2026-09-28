from aiogram.fsm.state import State, StatesGroup

class Profile(StatesGroup):
    name = State()
    age = State()
    gender = State()