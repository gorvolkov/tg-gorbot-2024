from keyboards.inline import main_menu_kbd
from loader import bot
from pagination import init_pagination
from states.states import SearchState
from telebot.types import Message


from api import get_by_rating
from config_data.config import GENRES_SET
from database.db_interface import write_selection_to_temp, merge_temp_to_movies
from config_data.config import no_result_answer


@bot.callback_query_handler(func=lambda call: (call.data == "movies_by_rating"))
def ask_genre(call):
    """Хэндлер для запуска поиска фильмов по рейтингу (первый шаг сценария).
    Запрашивается жанр"""

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Введите жанр: ')
    bot.set_state(call.from_user.id, SearchState.r_genre)


@bot.message_handler(state=SearchState.r_genre)
def ask_rating(message: Message) -> None:
    """Хэндлер сценария поиска фильмов по рейтингу (второй шаг сценария).
        Выполняется проверка корректности введённого жанра,
        в случае успеха запрашивается рейтинг"""

    query_genre = message.text.lower()
    if query_genre not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, введите корректный жанр: ")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = query_genre
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

            write_selection_to_temp(movie_list=result, user_id=message.from_user.id)
            first_result = str(result[0])
            kbd = init_pagination(count=len(result), user_id=message.from_user.id)
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу:\n {first_result}',
                             reply_markup=kbd)

            # if result:
            #     write_selection_to_temp(movie_list=result, user_id=message.from_user.id)
            #     first_result = str(result[0])
            #     kbd = init_pagination(count=len(result), user_id=message.from_user.id)
            #     bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу:\n {first_result}',
            #                      reply_markup=kbd)
            # else:
            #     bot.send_message(message.from_user.id, no_result_answer, reply_markup=main_menu_kbd())


@bot.callback_query_handler(state=SearchState.r_count, func=lambda call: (call.data == "continue"))
def continue_current_mode(call):
    """Хэндлер для повторного запуска сценария поиска фильмов по рейтингу"""

    merge_temp_to_movies()

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Введите жанр: ')
    bot.set_state(call.from_user.id, SearchState.r_genre)
