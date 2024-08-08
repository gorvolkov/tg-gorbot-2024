from loader import bot
from states.states import SearchState
from telebot.types import Message

from api import get_high_budget
from config_data.config import GENRES_SET
from database.write_movie_to_db import write_to_db
from keyboards.inline.mid_menu import gen_mid_menu


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "high_budget_movies"))
def ask_genre(callback_query):
    """Хэндлер сценария поиска фильмов с высоким бюджетом (первый шаг сценария).
    Запрашивает жанр"""

    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.hb_genre)


@bot.message_handler(state=SearchState.hb_genre)
def ask_count(message: Message) -> None:
    """Хэндлер сценария поиска фильмов с высоким бюджетом (второй шаг сценария).
        Выполняется проверка корректности введённого жанра,
        в случае успеха запрашивается кол-во фильмов в выборке"""

    if message.text.lower() not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, подумайте ещё")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, SearchState.hb_count, message.chat.id)


@bot.message_handler(state=SearchState.hb_count)
def give_result(message: Message) -> None:
    """Хэндлер сценария поиска фильмов с высоким бюджетом (заключительный шаг сценария).
        Выполняется проверка корректности введённого значения кол-ва фильмов в выборке.
        В случае успеха отдается результат"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_high_budget(genre=data['genre'], count=data['count'])
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу:\n\n')
            for movie in result:
                write_to_db(movie=movie, user_id=message.from_user.id)
                bot.send_message(message.from_user.id, f'{str(movie)}')
        bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())


@bot.callback_query_handler(state=SearchState.hb_count,
                            func=lambda callback_query: (callback_query.data == "continue"))
def continue_current_mode(callback_query) -> None:
    """Хэндлер для повторного запуска сценария поиска фильмов с высоким бюджетом"""

    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.hb_genre)
