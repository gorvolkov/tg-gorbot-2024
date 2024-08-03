from telebot.types import Message
from loader import bot
from states.states import SearchState


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "quit"))
def movie_by_title_answer(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, f"До свидания, {callback_query.from_user.full_name}!\n"
                          f"Надеюсь, я помог вам с выбором фильма для просмотра")
    bot.set_state(callback_query.from_user.id, SearchState.awaiting)


# @bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_main"))
# def from_mid_to_main(callback_query):
#     bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
#     bot.send_message(callback_query.from_user.id, 'Здесь будет вызов главного меню')