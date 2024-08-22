from database.models import Movie, Temp, User
from database.db_interface import merge_temp_to_movies
from loader import bot
from keyboards.inline import main_menu_kbd, pagination_kbd
from states.states import SearchState


@bot.callback_query_handler(func=lambda call: (call.data == "to_main"))
def return_to_main_menu(call):
    """Хэндлер, обрабатывающий команду возврата в главное меню"""
    merge_temp_to_movies()

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Выберите направление поиска", reply_markup=main_menu_kbd())


@bot.callback_query_handler(func=lambda call: (call.data == "quit"))
def quit_bot(call):
    """Обработчик завершения работы с ботом"""

    merge_temp_to_movies()

    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, f"До свидания, {call.from_user.full_name}!\n"
                                        f"Надеюсь, я помог вам с выбором фильма для просмотра.")

    # проверить, нужен ли этот стейт
    bot.set_state(call.from_user.id, SearchState.awaiting)


@bot.callback_query_handler(func=lambda call: (call.data.startswith('pagination')))
def process_pagination(call) -> None:
    """Хэндлер для навигации по полученной выборке поиска"""

    req = call.data.split('_')
    mode, page, count = req[1], int(req[2]), int(req[3])

    if mode == 'backward' and page != 1:
        page -= 1
    elif mode == 'forward' and page != count:
        page += 1

    curr_result = str(Temp.get(Temp.movie_id == page))
    new_kbd = pagination_kbd(page=page, count=count)
    bot.send_message(call.from_user.id, curr_result, reply_markup=new_kbd)
