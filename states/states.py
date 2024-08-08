from telebot.handler_backends import State, StatesGroup


class SearchState(StatesGroup):
    n_name = State()
    n_count = State()

    r_genre = State()
    r_rating = State()
    r_count = State()

    hb_genre = State()
    hb_count = State()

    lb_genre = State()
    lb_count = State()

    h_date = State()

    awaiting = State()
