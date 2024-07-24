from aiogram.fsm.state import StatesGroup, State


class AddSite(StatesGroup):
    site = State()


class AddProxy(StatesGroup):
    proxy = State()
