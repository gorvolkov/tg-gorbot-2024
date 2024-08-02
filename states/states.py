from telebot.handler_backends import State, StatesGroup


class SearchState(StatesGroup):
    title = State()
    hb_genre = State()
    hb_count = State()
    lb_genre = State()
    lb_count = State()
    r_genre = State()
    r_count = State()
    history = ()
    awaiting = State()
