from telebot.types import InlineKeyboardMarkup
from keyboards.inline import pagination_kbd


def init_pagination(count: int) -> InlineKeyboardMarkup:
    """
    Функция, инициализирующая работу с пагинацией.
    Создает первую клавиатуру для навигации по текущей выборке фильмов.
    """

    first_pagination_kbd = pagination_kbd(page=1, count=count)
    return first_pagination_kbd
