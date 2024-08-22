from telebot.types import InlineKeyboardMarkup

from database.models import User
from keyboards.inline import pagination_kbd


def init_pagination(count: int, user_id: int) -> InlineKeyboardMarkup:
    """
    Функция, инициализирующая работу с пагинацией.
    Создает первую клавиатуру для навигации по текущей выборке фильмов.
    """

    user = User.get_or_none(User.user_id == user_id)
    last_movie_id = user.movies.select().count()
    first_pagination_kbd = pagination_kbd(page=1, count=count)

    return first_pagination_kbd
