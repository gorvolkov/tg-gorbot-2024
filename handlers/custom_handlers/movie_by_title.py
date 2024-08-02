from loader import bot
from states.states import SearchState
from telebot.types import Message

from api import get_movie_by_title
import keyboards



@bot.callback_query_handler(func=lambda callback_query: (callback_query.data in ["movie_by_title", "continue"]))
def ask_title(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    # направляем на сценарий поиска фильма по названию
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала')
    bot.set_state(callback_query.from_user.id, SearchState.title)


@bot.message_handler(state=SearchState.title)
def movie_search_response(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_query'] = message.text
        result = get_movie_by_title.get_movie_by_title(data['user_query'])
        bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')
    bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=keyboards.inline.mid_menu.gen_mid_menu())

    # bot.set_state(message.from_user.id, MovieSearchState.mid_state, message.chat.id)


# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "continue"))
# def from_mid_continue(callback_query):
#     ask_title()
#
#
@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_main"))
def from_mid_to_main(callback_query):
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, reply_markup=keyboards.inline.main_menu.gen_main_menu())
#
#
# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "quit"))
# def from_mid_to_quit(callback_query):
#     # Удаляем клавиатуру.
#     bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
#     bot.reply_to(callback_query.from_user.id, f"До свидания, {callback_query.from_user.full_name}!\n"
#                                               f"Надеюсь, я помог вам с выбором фильма для просмотра",
#                  callback_query.chat.id)
