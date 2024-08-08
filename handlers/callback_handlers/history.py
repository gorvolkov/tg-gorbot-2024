import datetime
from typing import List

from telebot.types import Message

from database.models import User, Movie
from keyboards.inline.mid_menu import gen_mid_menu
from loader import bot
from states.states import SearchState


DATE_FORMAT = "%d.%m.%Y"


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "history"))
def ask_date_for_history(callback_query):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.set_state(callback_query.from_user.id, SearchState.h_date)
    bot.send_message(callback_query.from_user.id, "Введите дату поиска (ДД.ММ.ГГГГ)")


@bot.message_handler(state=SearchState.h_date)
def give_history(message: Message):
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)

    due_date_string = message.text
    try:
        user_date = datetime.datetime.strptime(due_date_string, DATE_FORMAT)
    except ValueError:
        bot.send_message(message.from_user.id, "Введите дату поиска в правильном формате (ДД.ММ.ГГГГ):")
        return

    # можно дописать проверку, чтобы при вводе еще не наступившей даты бот отвечал, что этот день еще не наступил и т.п.

    history = user.movies.filter(due_date=user_date).order_by(-Movie.movie_id)
    # result.extend(map(str, reversed(movies)))

    if not history:
        bot.send_message(message.from_user.id, "На эту дату ничего не нашлось", reply_markup=gen_mid_menu())
        return
    else:
        # вот это уже огород. когда будет пагинация, это все не нужно будет
        if len(history) > 1:
            for movie in history[::-2]:
                bot.send_message(message.from_user.id, f"{str(movie)}")
            bot.send_message(message.from_user.id, str(history[-1]), reply_markup=gen_mid_menu())
        else:
            bot.send_message(message.from_user.id, str(history[0]), reply_markup=gen_mid_menu())
        bot.set_state(message.from_user.id, SearchState.awaiting)




# @bot.callback_query_handler(state=SearchState.r_count, func=lambda callback_query: (callback_query.data == "continue"))
# def continue_current_mode(callback_query):
#     """Хэндлер для повторного запуска сценария поиска по истории"""
#
#     bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
#     bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
#     bot.set_state(callback_query.from_user.id, SearchState.r_genre)
