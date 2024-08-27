from telebot.types import Message

from api import get_by_name
from database.db_interface import write_selection_to_temp, merge_temp_to_movies
from config_data.config import no_result_answer
from loader import bot
from keyboards.inline import main_menu_kbd
from pagination import init_pagination
from states.states import SearchState


@bot.callback_query_handler(func=lambda call: (call.data == "movie_by_title"))
def ask_title(call) -> None:
    """Хэндлер для старта поиска по названию (1 шаг сценария). Запрашивается название фильма"""

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Введите название фильма или сериала: ")
    bot.set_state(call.from_user.id, SearchState.n_name)


@bot.message_handler(state=SearchState.n_name)
def ask_count(message: Message) -> None:
    """Хэндлер для продолжения поиска по названию (2 шаг сценария). Запрашивается кол-во фильмов в выборке"""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["name"] = message.text
    bot.set_state(message.from_user.id, SearchState.n_count)
    bot.send_message(message.from_user.id, "Введите кол-во фильмов в выборке:")


@bot.message_handler(state=SearchState.n_count)
def give_result(message: Message) -> None:
    """Хэндлер завершения поиска по названию"""

    if not message.text.isdigit():
        bot.send_message(
            message.from_user.id,
            "Здесь может быть только число. "
            "Пожалуйста, введите корректное значение:",
        )
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["count"] = message.text
            result = get_by_name(name=data["name"], count=data["count"])

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
    state=SearchState.n_count, func=lambda call: (call.data == "continue")
)
def continue_current_mode(call) -> None:
    """Хэндлер для повторного запуска поиска фильмов по названию"""

    merge_temp_to_movies()
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Введите название фильма или сериала:")
    bot.set_state(call.from_user.id, SearchState.n_name)
