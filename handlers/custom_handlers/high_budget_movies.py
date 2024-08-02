from loader import bot
from states.states import MovieSearchState
from telebot.types import Message

from api import get_high_budget_movies
from config_data.config import GENRES_SET


@bot.message_handler(commands=['high_budget_movie'])
def ask_genre(message: Message) -> None:
    bot.send_message(message.from_user.id, "Введите жанр:")
    bot.set_state(message.from_user.id, MovieSearchState.high_budget_genre, message.chat.id)


@bot.message_handler(state=MovieSearchState.high_budget_genre)
def ask_count(message: Message) -> None:
    if message.text.lower() not in GENRES_SET:
        bot.send_message(message.from_user.id, "Такого жанра нет в моём каталоге. Пожалуйста, подумайте ещё")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genre'] = message.text
        bot.send_message(message.from_user.id, 'Введите количество фильмов в выборке:')
        bot.set_state(message.from_user.id, MovieSearchState.high_budget_count, message.chat.id)


@bot.message_handler(state=MovieSearchState.high_budget_count)
def give_result(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_high_budget_movies.get_high_budget_movies(genre=data['genre'], count=data['count'])
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n {result}')

            bot.set_state(message.from_user.id, MovieSearchState.high_budget_genre, message.chat.id)
            # bot.set_state(message.from_user.id, MovieSearchState.mid_menu, message.chat.id)
#           пока нет промежуточного меню, возвращаю первое состояние текущего сценария