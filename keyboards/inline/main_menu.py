from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_main_menu() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text="Поиск по названию", callback_data="movie_by_title")
    button_2 = InlineKeyboardButton(text="Поиск по рейтингу", callback_data="movies_by_rating")
    button_3 = InlineKeyboardButton(text="Выс. бюджет", callback_data="high_budget_movies")
    button_4 = InlineKeyboardButton(text="Низ. бюджет", callback_data="low_budget_movies")
    button_5 = InlineKeyboardButton(text="История", callback_data="history")
    button_6 = InlineKeyboardButton(text="Завершить", callback_data="quit")

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard
