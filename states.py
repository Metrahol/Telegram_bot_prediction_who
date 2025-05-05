
from aiogram.fsm.state import State, StatesGroup


class TestStates(StatesGroup):
    """
    Определяет состояния конечного автомата (FSM) для процесса прохождения теста.
    """
    answering = State()
