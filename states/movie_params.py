from telebot.handler_backends import State, StatesGroup


class MovieInfoState(StatesGroup):
    title = State()
    genre = State()
    count = State()
