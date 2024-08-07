from loader import bot
from keyboards.inline.main_menu import gen_main_menu


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "to_main"))
def from_mid_to_main(callback_query):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, "Выберите направление поиска", reply_markup=gen_main_menu())
