from telebot.handler_backends import State, StatesGroup


class MovieInfoState(StatesGroup):
    genre = State()
    count = State()
