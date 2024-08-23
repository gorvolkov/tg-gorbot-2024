from telebot.types import Message

from keyboards.inline import main_menu_kbd
from loader import bot
from pagination import init_pagination
from states.states import SearchState
from api import get_by_budget
from config_data.config import GENRES_SET, no_result_answer
from database.db_interface import write_selection_to_temp, merge_temp_to_movies


@bot.callback_query_handler(func=lambda call: (call.data == "high_budget_movies"))
def ask_genre(call):
    """Хэндлер сценария поиска фильмов с высоким бюджетом (первый шаг сценария).
    Запрашивает жанр"""

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Введите жанр: ")
    bot.set_state(call.from_user.id, SearchState.hb_genre)


@bot.message_handler(state=SearchState.hb_genre)
def ask_count(message: Message) -> None:
    """Хэндлер сценария поиска фильмов с высоким бюджетом (второй шаг сценария).
    Выполняется проверка корректности введённого жанра,
    в случае успеха запрашивается кол-во фильмов в выборке"""

    if message.text.lower() not in GENRES_SET:
        bot.send_message(
            message.from_user.id,
            "Такого жанра нет в моём каталоге. Пожалуйста, введите корректный жанр.",
        )
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"] = message.text.lower()
        bot.send_message(message.from_user.id, "Введите количество фильмов в выборке:")
        bot.set_state(message.from_user.id, SearchState.hb_count, message.chat.id)


@bot.message_handler(state=SearchState.hb_count)
def give_result(message: Message) -> None:
    """Хэндлер сценария поиска фильмов с высоким бюджетом (заключительный шаг сценария).
    Выполняется проверка корректности введённого значения кол-ва фильмов в выборке.
    В случае успеха отдается результат"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, "Здесь может быть только число")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["count"] = message.text
            result = get_by_budget(genre=data["genre"], count=data["count"])

            if result:
                write_selection_to_temp(movie_list=result, user_id=message.from_user.id)
                first_result = str(result[0])
                kbd = init_pagination(count=len(result))
                bot.send_message(
                    message.from_user.id,
                    f"Вот что нашлось по вашему запросу:\n {first_result}",
                    parse_mode="html",
                    reply_markup=kbd,
                )
            else:
                bot.send_message(
                    message.from_user.id, no_result_answer, reply_markup=main_menu_kbd()
                )


@bot.callback_query_handler(
    state=SearchState.hb_count, func=lambda call: (call.data == "continue")
)
def continue_current_mode(call) -> None:
    """Хэндлер для повторного запуска сценария поиска фильмов с высоким бюджетом"""

    merge_temp_to_movies()

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Введите жанр: ")
    bot.set_state(call.from_user.id, SearchState.hb_genre)
