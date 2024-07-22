from telebot.handler_backends import State, StatesGroup


class UserDialogState(StatesGroup):
    start_dialog = State()
    question_1 = State()
    question_2 = State()
    state_low = State()
    state_high = State()
    state_custom = State()