from config_data.config import no_result_answer
from database.db_interface import merge_temp_to_movies, get_history, write_selection_to_temp
from keyboards.inline import main_menu_kbd
from pagination import init_pagination
from utils.calendar import MyCalendar, cal_steps
from loader import bot
from states.states import SearchState


@bot.callback_query_handler(func=lambda call: (call.data == "history"))
def ask_date(call):
    """Хэндлер сценария запроса истории поиска (первый шаг сценария).
    Запрашивает дату, за которую нужно выдать историю поиска"""

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.set_state(call.from_user.id, SearchState.h_date)

    calendar, step = MyCalendar().build()
    bot.send_message(call.from_user.id, f"Выберите {cal_steps[step]}", reply_markup=calendar)


# @bot.message_handler(state=SearchState.h_date)
# def give_history(message: Message) -> None:
#     """Хэндлер сценария запроса истории поиска (второй шаг сценария).
#         Проверяет корректность введенной даты.
#         В случае прохождения проверки отправляет пользователю результат"""
#
#     user_id = message.from_user.id
#     user = User.get_or_none(User.user_id == user_id)
#
#     due_date_string = message.text
#     try:
#         user_date = datetime.datetime.strptime(due_date_string, DATE_FORMAT)
#     except ValueError:
#         bot.send_message(message.from_user.id, "Введите дату поиска в правильном формате (ДД.ММ.ГГГГ):")
#         return
#
#     # можно дописать проверку, чтобы при вводе еще не наступившей даты бот отвечал, что этот день еще не наступил и т.п.
#
#     history = user.movies.filter(due_date=user_date).order_by(-Movie.movie_id)
#     # result.extend(map(str, reversed(movies)))
#
#     if not history:
#         bot.send_message(message.from_user.id, "На эту дату ничего не нашлось", reply_markup=gen_mid_menu())
#         return
#     else:
#         if len(history) > 1:
#             for movie in history[:-1]:
#                 bot.send_message(message.from_user.id, f"{str(movie)}")
#             bot.send_message(message.from_user.id, str(history[-1]), reply_markup=gen_mid_menu())
#         else:
#             bot.send_message(message.from_user.id, str(history[0]), reply_markup=gen_mid_menu())
#         bot.set_state(message.from_user.id, SearchState.awaiting)


@bot.callback_query_handler(func=MyCalendar.func())
def calendar_handler(call):
    """
    Обработчик взаимодействия пользователя с календарем.
    Получает дату и выдает историю поиска пользователя за эту дату
    """

    query_date, key, step = MyCalendar().process(call.data)
    if not query_date and key:
        bot.edit_message_text(f"Выберите {cal_steps[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif query_date:

        result = get_history(user_id=call.from_user.id, date=query_date)

        if result:
            write_selection_to_temp(movie_list=result, user_id=call.from_user.id)
            first_result = str(result[0])
            kbd = init_pagination(count=len(result), user_id=call.from_user.id)
            bot.send_message(call.from_user.id, f'Вот что нашлось по вашему запросу:\n {first_result}',
                             reply_markup=kbd)
        else:
            bot.send_message(call.from_user.id, no_result_answer, reply_markup=main_menu_kbd())


@bot.callback_query_handler(state=SearchState.h_date, func=lambda call: (call.data == "continue"))
def continue_current_mode(call) -> None:
    """Хэндлер для повторного поиска по истории"""
    merge_temp_to_movies()

    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.set_state(call.from_user.id, SearchState.h_date)
    bot.send_message(call.from_user.id, "Введите дату поиска")
