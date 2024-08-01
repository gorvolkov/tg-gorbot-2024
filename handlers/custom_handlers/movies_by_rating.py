from loader import bot
from states.movie_params import MovieInfoState
from telebot.types import Message


@bot.message_handler(commands=['movie_by_rating'])
def get_genre(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.username}! Введите жанр')
    bot.set_state(message.from_user.id, MovieInfoState.genre, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['genre'] = message.text


@bot.message_handler(state=MovieInfoState.genre)
def get_count(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, MovieInfoState.count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Здесь может быть только число')




