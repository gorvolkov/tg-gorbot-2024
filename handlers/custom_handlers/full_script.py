from telebot.types import Message

from loader import bot

from keyboards.inline.mid_menu import gen_mid_menu
from keyboards.inline.main_menu import gen_main_menu

from states.states import SearchState, SearchDirection

from api import get_movie_by_title, get_high_budget_movies, get_low_budget_movies, get_movies_by_rating
from config_data.config import GENRES_SET

@bot.message_handler(commands=["start"])
def greeting(message: Message):
    bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! "
                                           f"Это бот Кинопоиска, который поможет вам сориентироваться в мире кинематографа.\n"
                                           f"Я выполняю следующие команды:\n\n"
                                           f"/movie_search — поиск фильма/сериала по названию\n"
                                           f"/movie_by_rating — поиск фильмов/сериалов по рейтингу\n"
                                           f"/low_budget_movie — поиск фильмов/сериалов с низким бюджетом\n"
                                           f"/high_budget_movie — поиск фильмов/сериалов с высоким бюджетом\n"
                                           f"/history — просмотр истории ваших запросов и поиска фильма/сериала\n\n"
                                           f"Выберите направление поиска", reply_markup=gen_main_menu())


# обработчики главного меню
@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "movie_by_title"))
def ask_title(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    # направляем на сценарий поиска фильма по названию
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала')
    bot.set_state(callback_query.from_user.id, SearchDirection.title)

@bot.message_handler(state=SearchDirection.title)
def single_movie_info(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_query'] = message.text
        result = get_movie_by_title.get_movie_by_title(data['user_query'])
        bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')
        bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())

def ask_genre(callback_query) -> None:
    bot.send_message(callback_query.from_user.id, "Введите жанр:")
    bot.set_state(callback_query.from_user.id, SearchState.genre)

@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "movie_by_rating"))
def movie_by_rating_ask(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchDirection.rating, callback_query.chat.id)
    ask_genre(callback_query)

@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "low_budget_movies"))
def low_budget_movies(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchDirection.low_budget, callback_query.chat.id)
    ask_genre(callback_query)


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "high_budget_movies"))
def low_budget_movies(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchDirection.high_budget, callback_query.chat.id)
    ask_genre(callback_query)


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "history"))
def low_budget_movies(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchDirection.history, callback_query.chat.id)
    bot.send_message(callback_query.from_user.id, "эта функция пока не работает", callback_query.chat.id)


@bot.message_handler(state=SearchState.genre)
def get_genre(message: Message) -> None:
    if message.text.lower() not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, подумайте ещё")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, SearchState.count, message.chat.id)


@bot.message_handler(states=[SearchState.count, SearchDirection.rating])
def get_count(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_movies_by_rating.get_movies_by_rating(genre=data['genre'], count=data['count'])
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')











# промежуточное меню
# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "continue"))
# def from_mid_continue(callback_query):
#     ask_title()
#
#
# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_main"))
# def from_mid_to_main(callback_query):
#     bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
#     bot.send_message(callback_query.from_user.id, reply_markup=gen_main_menu())
#
#
# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "quit"))
# def from_mid_to_quit(callback_query):
#     # Удаляем клавиатуру.
#     bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
#     bot.reply_to(callback_query.from_user.id, f"До свидания, {callback_query.from_user.full_name}!\n"
#                                               f"Надеюсь, я помог вам с выбором фильма для просмотра",
#                  callback_query.chat.id)
