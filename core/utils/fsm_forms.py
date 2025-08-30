from aiogram.fsm.state import StatesGroup, State


class ApplicationForm(StatesGroup):
    name = State()
    service = State()
    details = State()
    file = State()
    contact = State()
    username = State()
    phone_number = State()
    confirm = State()
