from loader import bot
from states.movie_params import MovieInfoState
from telebot.types import Message

from api import get_movie_by_title


@bot.message_handler(commands=['movie_search'])
def movie_search_hello(message: Message) -> None:
    bot.set_state(message.from_user.id, MovieInfoState.title, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.username}! '
                                           f'Введите название фильма или сериала')


@bot.message_handler(state=MovieInfoState.title)
def movie_search_response(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_query'] = message.text
        result = get_movie_by_title.get_movie_by_title(data['user_query'])
        bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу\n\n', result)

# выкинуть клавиатуру с вариантами - продолжить или вернуться в главное меню