from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kbd() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""

    button_1 = InlineKeyboardButton(text="Поиск по названию", callback_data="movie_by_title")
    button_2 = InlineKeyboardButton(text="Поиск по рейтингу", callback_data="movies_by_rating")
    button_3 = InlineKeyboardButton(text="Выс. бюджет", callback_data="high_budget_movies")
    button_4 = InlineKeyboardButton(text="Низ. бюджет", callback_data="low_budget_movies")
    button_5 = InlineKeyboardButton(text="История", callback_data="history")
    button_6 = InlineKeyboardButton(text="Завершить", callback_data="quit")

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard


def pagination_kbd(page: int, count: int) -> InlineKeyboardMarkup:
    """Клавиатура работы с полученной выборкой фильмов.
    Вторым рядом кнопок реализованы опции нового поиска по выбранному сценарию, завершения работы с ботом или возврата в главное меню
    """

    button_1 = InlineKeyboardButton(text=f'<-', callback_data=f"pagination_backward_{page}_{count}")
    button_2 = InlineKeyboardButton(text=f"{page}/{count}", callback_data="_")
    button_3 = InlineKeyboardButton(text=f'->', callback_data=f"pagination_forward_{page}_{count}")
    button_4 = InlineKeyboardButton(text="Продолжить", callback_data="continue")
    button_5 = InlineKeyboardButton(text="Завершить", callback_data="quit")
    button_6 = InlineKeyboardButton(text="В главное меню", callback_data="to_main")

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard
