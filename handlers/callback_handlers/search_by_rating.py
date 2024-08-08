from loader import bot
from states.states import SearchState
from telebot.types import Message

from api import get_by_rating
from config_data.config import GENRES_SET
from database.write_movie_to_db import write_to_db
from keyboards.inline.mid_menu import gen_mid_menu


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "movies_by_rating"))
def ask_genre(callback_query):
    """Хэндлер для запуска поиска фильмов по рейтингу (первый шаг сценария).
    Запрашивается жанр"""

    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.r_genre)


@bot.message_handler(state=SearchState.r_genre)
def ask_rating(message: Message) -> None:
    """Хэндлер сценария поиска фильмов по рейтингу (второй шаг сценария).
        Выполняется проверка корректности введённого жанра,
        в случае успеха запрашивается рейтинг"""

    if message.text.lower() not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, введите корректный жанр: ")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id, 'Введите рейтинг (число от 1 до 10):')
        bot.set_state(message.from_user.id, SearchState.r_rating, message.chat.id)


@bot.message_handler(state=SearchState.r_rating)
def ask_count(message: Message) -> None:
    """Хэндлер сценария поиска фильмов по рейтингу (третий шаг сценария).
        Выполняется проверка корректности введённого значения рейтинга,
        в случае успеха запрашивается кол-во фильмов в выборке"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число от 1 до 10')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['rating'] = message.text
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, SearchState.r_count, message.chat.id)


@bot.message_handler(state=SearchState.r_count)
def give_result(message: Message) -> None:
    """Хэндлер сценария поиска фильмов по рейтингу (заключительный шаг сценария).
        Выполняется проверка корректности введённого значения кол-ва фильмов в выборке.
        В случае успеха отдается результат"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_by_rating(genre=data['genre'], rating=data['rating'], count=data['count'])
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу:\n\n')
            for movie in result:
                write_to_db(movie=movie, user_id=message.from_user.id)
                bot.send_message(message.from_user.id, f'{str(movie)}')
        bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())


@bot.callback_query_handler(state=SearchState.r_count, func=lambda callback_query: (callback_query.data == "continue"))
def continue_current_mode(callback_query):
    """Хэндлер для повторного запуска сценария поиска фильмов по рейтингу"""

    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.r_genre)
