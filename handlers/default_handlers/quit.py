from telebot.types import Message
from loader import bot


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == 'quit'))
def movie_by_title_answer(callback_query, message: Message):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
    bot.reply_to(message.from_user.id, f"До свидания, {message.from_user.full_name}!\n"
                          f"Надеюсь, я помог вам с выбором фильма для просмотра", message.chat.id)