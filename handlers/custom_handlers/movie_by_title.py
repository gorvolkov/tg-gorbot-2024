from loader import bot
from states.states import SearchState
from telebot.types import Message

from api import get_movie_by_title
from keyboards.inline.mid_menu import gen_mid_menu
from keyboards.inline.main_menu import gen_main_menu


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "movie_by_title"))
def ask_title(callback_query):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала')
    bot.set_state(callback_query.from_user.id, SearchState.title)


@bot.message_handler(state=SearchState.title)
def movie_search_response(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_query'] = message.text
        result = get_movie_by_title.get_movie_by_title(data['user_query'])
        bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')

    bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())


@bot.callback_query_handler(state=SearchState.title, func=lambda callback_query: (callback_query.data == "continue"))
def continue_current_mode(callback_query):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала')
    bot.set_state(callback_query.from_user.id, SearchState.title)




