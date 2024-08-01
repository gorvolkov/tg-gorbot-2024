from loader import bot
from states.states import MovieSearchState
from telebot.types import Message

from api import get_movies_by_rating


@bot.message_handler(commands=['movie_by_rating'])
def ask_genre(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введите жанр:")
    bot.set_state(message.from_user.id, MovieSearchState.rating_genre, message.chat.id)

    #  добавить проверку на соответствие тем жанрам, которые есть в каталоге Кинопоиска

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['genre'] = message.text


@bot.message_handler(state=MovieSearchState.rating_genre)
def ask_count(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, MovieSearchState.rating_count, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Здесь может быть только число')


@bot.message_handler(state=MovieSearchState.rating_count)
def rating_search(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        result = get_movies_by_rating.get_movies_by_rating(genre=data['genre'], count=data['count'])
        bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')
    # bot.set_state(message.from_user.id, MovieSearchState.mid_state, message.chat.id)






