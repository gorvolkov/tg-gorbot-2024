from telegram_bot_calendar import DetailedTelegramCalendar

from config_data.config import no_result_answer
from database.db_interface import (
    drop_temp,
    get_history,
    write_selection_to_temp,
)
from keyboards.inline import main_menu_kbd
from pagination import init_pagination
from loader import bot
from states.states import SearchState

cal_steps = {"y": "год", "m": "месяц", "d": "день"}


@bot.callback_query_handler(func=lambda call: (call.data == "history"))
def ask_date(call):
    """Хэндлер сценария запроса истории поиска (первый шаг сценария).
    Запрашивает дату, за которую нужно выдать историю поиска"""

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.set_state(call.from_user.id, SearchState.h_date)

    calendar, step = DetailedTelegramCalendar(locale="ru").build()
    bot.send_message(
        call.from_user.id, f"Выберите {cal_steps[step]}", reply_markup=calendar
    )


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def calendar_handler(call):
    """
    Обработчик взаимодействия пользователя с календарем.
    Получает дату и выдает историю поиска пользователя за эту дату
    """

    query_date, key, step = DetailedTelegramCalendar(locale="ru").process(call.data)
    if not query_date and key:
        bot.edit_message_text(
            f"Выберите {cal_steps[step]}",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=key,
        )
    elif query_date:
        result = get_history(user_id=call.from_user.id, query_date=query_date)

        if result:
            write_selection_to_temp(movie_list=result, user_id=call.from_user.id)
            first_result = str(result[0])
            kbd = init_pagination(count=len(result))
            bot.send_message(
                call.from_user.id,
                f"Вот что нашлось по вашему запросу:\n {first_result}",
                parse_mode="html",
                reply_markup=kbd,
            )
            bot.set_state(call.from_user.id, SearchState.from_history)
        else:
            bot.send_message(
                call.from_user.id, no_result_answer, reply_markup=main_menu_kbd()
            )


@bot.callback_query_handler(
    state=SearchState.from_history, func=lambda call: (call.data == "continue")
)
def continue_current_mode(call) -> None:
    """Хэндлер для повторного поиска по истории"""

    drop_temp()
    # в случае выхода из текущего сценария поиска по истории просто очищаем temp

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.set_state(call.from_user.id, SearchState.h_date)
    bot.send_message(call.from_user.id, "Введите дату поиска")
