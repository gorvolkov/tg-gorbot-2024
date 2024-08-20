from telebot.types import InlineKeyboardMarkup

from database.models import User, Movie
from keyboards.inline.pagination_kbd import gen_pagination_kbd
from keyboards.inline.mid_menu import gen_mid_menu
from loader import bot


def init_pagination(count: int, user_id: int) -> InlineKeyboardMarkup:
    """
    Функция, инициализирующая работу с пагинацией.
    Создает первую клавиатуру для навигации по текущей выборке фильмов.
    """

    user = User.get_or_none(User.user_id == user_id)
    last_movie_id = user.movies.select().count()
    first_pagination_kbd = gen_pagination_kbd(page=1, movie_id=last_movie_id + 1, count=count)

    return first_pagination_kbd


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data.startswith('pagination')))
def process_pagination(callback_query) -> None:
    """Хэндлер для работы с пагинацией"""

    req = callback_query.data.split('_')

    if req[1] == 'quit':
        bot.send_message(callback_query.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())
        return

    mode, page, movie_id, count = req[1], req[2], req[3], req[4]
    user_id = callback_query.from_user.id
    user = User.get_or_none(User.user_id == user_id)

    if mode == 'backward' and page != 1:
        # искать здесь
        new_result = user.movies.get(user.movies.movie_id == movie_id)


        new_kbd = gen_pagination_kbd(page=page - 1, movie_id=movie_id - 1, count=count)
        bot.send_message(callback_query.from_user.id, new_result, reply_markup=new_kbd)

    elif mode == 'forward' and page != count:
        # и здесь
        new_result = user.movies.get(user.movies.movie_id == movie_id)


        new_kbd = gen_pagination_kbd(page=page + 1, movie_id=movie_id + 1, count=count)
        bot.send_message(callback_query.from_user.id, new_result, reply_markup=new_kbd)








