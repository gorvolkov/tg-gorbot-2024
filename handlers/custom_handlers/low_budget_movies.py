from loader import bot
from states.states import SearchState
from telebot.types import Message

from api import get_low_budget_movies
from config_data.config import GENRES_SET
from keyboards.inline.mid_menu import gen_mid_menu


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "low_budget_movies"))
def movie_by_title_answer(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.lb_genre)


@bot.message_handler(state=SearchState.lb_genre)
def ask_count(message: Message) -> None:
    if message.text.lower() not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, подумайте ещё")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, SearchState.lb_count, message.chat.id)


@bot.message_handler(state=SearchState.lb_count)
def give_result(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_low_budget_movies.get_low_budget_movies(genre=data['genre'], count=data['count'])
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')

        bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())


@bot.callback_query_handler(state=SearchState.lb_count,
                            func=lambda callback_query: (callback_query.data == "continue"))
def continue_current_mode(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите жанр: ')
    bot.set_state(callback_query.from_user.id, SearchState.lb_genre)
