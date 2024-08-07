import datetime
from typing import List

from telebot.types import Message

import database
from database import User, Movie, History
from keyboards.inline.mid_menu import gen_mid_menu
from loader import bot
from states.states import SearchState
from keyboards.inline.pagination import gen_pagination_kbd

DATE_FORMAT = "%d.%m.%Y"


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "history"))
def ask_date_for_history(callback_query):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchState.h_date)
    bot.send_message(callback_query.from_user.id, "Введите дату поиска (ДД.ММ.ГГГГ)")


# @bot.message_handler(state=SearchState.h_date)
# def give_history(message: Message):
#     user_id = message.from_user.id
#     user = User.get_or_none(User.user_id == user_id)
#
#     due_date_string = message.text
#     try:
#         history_date = datetime.datetime.strptime(due_date_string, DATE_FORMAT)
#     except ValueError:
#         bot.send_message(message.from_user.id, "Введите дату поиска в правильном формате (ДД.ММ.ГГГГ):")
#         return
#
#     with bot.retrieve_data(message.from_user.id) as data:
#         data["due_date"] = due_date_string
#
#     result = []
#     movies: List[Movie] = user.movies.order_by(-Movie.due_date, -Movie.movie_id).limit(10)
#     result.extend(map(str, reversed(movies)))
#
#     if not result:
#         bot.send_message(message.from_user.id, "В вашей истории поиска ещё ничего нет")
#         return
#
#     bot.send_message(message.from_user.id, "\n\n".join(result), reply_markup=gen_mid_menu())
#     bot.set_state(message.from_user.id, SearchState.awaiting)

@bot.message_handler(state=SearchState.h_date)
def give_history(message: Message):
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)

    due_date_string = message.text
    try:
        user_date = datetime.datetime.strptime(due_date_string, DATE_FORMAT)
    except ValueError:
        bot.send_message(message.from_user.id, "Введите дату поиска в правильном формате (ДД.ММ.ГГГГ):")
        return

    movies: List[Movie] = user.movies.filter(due_date=user_date).order_by(-Movie.movie_id)
    for movie in movies:
        History.create(
            title=movie.title,
            title_orig=movie.title_orig,
            description=movie.description,
            rating=movie.rating,
            year=movie.year,
            genres=movie.genres,
            age_rating=movie.age_rating,
            poster=movie.poster)


    curr_page = None  # номер текущей страницы
    from_pages = None  # кол-во страниц в выборке всего

    if not movies:
        bot.send_message(message.from_user.id, "В вашей истории поиска ещё ничего нет")
        return

    # bot.send_message(message.from_user.id, "\n\n".join(result), reply_markup=gen_mid_menu())
    # bot.send_message(message.from_user.id, "\n\n".join(result), reply_markup=gen_pagination_kbd())
    bot.set_state(message.from_user.id, SearchState.awaiting)


# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_left_page"))
# def to_left_page(callback_query, history_data):
#
#
#
#
# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_right_page"))
# def to_right_page(callback_query, hisote):
#     bot.delete_message(callback_query.chat.id, previous_message.id)
#     bot.send_message(callback_query.from_user.id, "Выберите направление поиска", reply_markup=gen_main_menu())


# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "from_hist_to_main"))
# def to_left_page(callback_query):
#     History.delete().execute()


entity = History.delete()
print(entity)

