from telebot.types import Message, CallbackQuery

from api import get_by_budget
from database.db_interface import write_selection_to_temp, merge_temp_to_movies
from config_data.config import no_result_answer
from keyboards.inline import main_menu_kbd
from keyboards.inline.inline_keyboards import genres_kbd
from loader import bot
from pagination import init_pagination
from states.states import SearchState


@bot.callback_query_handler(func=lambda call: (call.data == "low_budget"))
def ask_genre(call: CallbackQuery):
    """Хэндлер сценария поиска фильмов с высоким бюджетом (первый шаг сценария).
    Запрашивается жанр"""

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Выберите жанр: ", reply_markup=genres_kbd())
    bot.set_state(call.from_user.id, SearchState.lb_genre)


@bot.callback_query_handler(
    state=SearchState.lb_genre, func=lambda call: (call.data.startswith("genre"))
)
def ask_count(call: CallbackQuery) -> None:
    """Хэндлер сценария поиска фильмов с высоким бюджетом (второй шаг сценария).
    Запрашивается кол-во результатов в выборке"""

    bot.delete_message(call.from_user.id, call.message.id)
    query_genre = call.data.split("_")[1]

    with bot.retrieve_data(call.from_user.id) as data:
        data["genre"] = query_genre

    bot.send_message(call.from_user.id, "Введите количество фильмов в выборке:")
    bot.set_state(call.from_user.id, SearchState.lb_count)


@bot.message_handler(state=SearchState.lb_count)
def give_result(message: Message) -> None:
    """Хэндлер сценария поиска фильмов с низким бюджетом (заключительный шаг сценария).
    Выполняется проверка корректности введённого значения кол-ва фильмов в выборке.
    В случае успеха отдается результат"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, "Здесь может быть только число")
    else:
        with bot.retrieve_data(message.from_user.id) as data:
            data["count"] = message.text
            result = get_by_budget(genre=data["genre"], count=data["count"], low=True)

            if result:
                write_selection_to_temp(movie_list=result, user_id=message.from_user.id)
                first_result = str(result[0])
                kbd = init_pagination(count=len(result))
                bot.send_message(
                    message.from_user.id,
                    f"Вот что нашлось по вашему запросу:\n\n{first_result}",
                    parse_mode="html",
                    reply_markup=kbd,
                )
            else:
                bot.send_message(
                    message.from_user.id, no_result_answer, reply_markup=main_menu_kbd()
                )


@bot.callback_query_handler(
    state=SearchState.lb_count, func=lambda call: (call.data == "continue")
)
def continue_current_mode(call: CallbackQuery) -> None:
    """Хэндлер для повторного запуска сценария поиска фильмов с низким бюджетом"""
    merge_temp_to_movies()

    bot.edit_message_reply_markup(call.from_user.id, call.message.id)
    bot.send_message(call.from_user.id, "Выберите жанр: ", reply_markup=genres_kbd())
    bot.set_state(call.from_user.id, SearchState.lb_genre)
