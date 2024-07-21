from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['movie_search'])
def movie_search(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.username}! '
                                           f'Введите название фильма или сериала, информацию о котором вы хотите найти')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['title'] = message.text

#     далее какое-то взаимодействие через api и возврат результата пользователю

