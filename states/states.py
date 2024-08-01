from telebot.handler_backends import State, StatesGroup


class MovieSearchState(StatesGroup):
    start_state = State()
    mid_state = State()
    end_state = State()

    title = State()

    high_budget_genre = State()
    high_budget_count = State()

    low_budget_genre = State()
    low_budget_count = State()

    rating_genre = State()
    rating_count = State()
    