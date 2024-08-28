from database.models import Temp
from database.db_interface import merge_temp_to_movies, drop_temp
from loader import bot
from keyboards.inline import main_menu_kbd, pagination_kbd
from states.states import SearchState


@bot.callback_query_handler(
    state=SearchState.from_history, func=lambda call: (call.data == "to_main")
)
def to_main_from_history(call) -> None:
    """Хэндлер, обрабатывающий команду возврата в главное меню из сценария поиска по истории"""

    drop_temp()
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    # убираем клавиатуру, но оставляем в чате последний просмотренный вариант:
    # вдруг пользователь захочет быстро вернуться к нему; тогда ему будет достаточно просто пролистать вверх чат

    bot.send_message(
        call.from_user.id, "Выберите направление поиска", reply_markup=main_menu_kbd()
    )


@bot.callback_query_handler(func=lambda call: (call.data == "to_main"))
def return_to_main_menu(call) -> None:
    """Хэндлер, обрабатывающий команду возврата в главное меню"""

    merge_temp_to_movies()
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id, "Выберите направление поиска", reply_markup=main_menu_kbd()
    )


@bot.callback_query_handler(
    state=SearchState.from_history, func=lambda call: (call.data == "quit")
)
def quit_from_history(call) -> None:
    """Хэндлер, обрабатывающий завершение работы с ботом из сценария поиска по истории"""

    drop_temp()
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id,
        f"До свидания, {call.from_user.full_name}!\n"
        f"Надеюсь, я помог вам с выбором фильма для просмотра.",
    )

    bot.set_state(call.from_user.id, SearchState.awaiting)


@bot.callback_query_handler(func=lambda call: (call.data == "quit"))
def quit_bot(call) -> None:
    """Хэндлер завершения работы с ботом"""

    merge_temp_to_movies()
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id,
        f"До свидания, {call.from_user.full_name}!\n"
        f"Надеюсь, я помог вам с выбором фильма для просмотра.",
    )

    bot.set_state(call.from_user.id, SearchState.awaiting)


@bot.callback_query_handler(func=lambda call: (call.data.startswith("pagination")))
def process_pagination(call) -> None:
    """Хэндлер для навигации по полученной выборке поиска"""

    req = call.data.split("_")
    mode, page, count = req[1], int(req[2]), int(req[3])

    if mode == "backward" and page != 1:
        page -= 1
    elif mode == "forward" and page != count:
        page += 1

    curr_result = str(Temp.get(Temp.movie_id == page))
    new_kbd = pagination_kbd(page=page, count=count)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id, curr_result, parse_mode="html", reply_markup=new_kbd
    )
