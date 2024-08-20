from datetime import datetime

from states.states import SearchState
from telebot.types import Message


from api import get_by_name

from database.write_movie_to_db import write_to_db
from loader import bot
from keyboards.inline.mid_menu import gen_mid_menu
from pagination import init_pagination


@bot.callback_query_handler(func=lambda callback_query: (callback_query.data == "movie_by_title"))
def ask_title(callback_query) -> None:
    """Хэндлер для старта поиска по названию. Спрашиваем название фильма"""

    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала: ')
    bot.set_state(callback_query.from_user.id, SearchState.n_name)


@bot.message_handler(state=SearchState.n_name)
def ask_count(message: Message) -> None:
    """Хэндлер для продолжения поиска по названию. Спрашиваем кол-во фильмов в выборке"""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.set_state(message.from_user.id, SearchState.n_count)
    bot.send_message(message.from_user.id, 'Введите кол-во фильмов в выборке: ')


@bot.message_handler(state=SearchState.n_count)
def give_result(message: Message) -> None:
    """Хэндлер завершения поиска по названию. Выдаем пользователю результат"""

    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Здесь может быть только число')
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count'] = message.text
            result = get_by_name(name=data['name'], count=data['count'])
            for movie in result:
                write_to_db(movie=movie, user_id=message.from_user.id)
            #     записали все в базу данных. это можно включить в функцию получения результата

            first_result = str(result[0])
            kbd = init_pagination(count=len(result), user_id=message.from_user.id)
            bot.send_message(message.from_user.id, f'Вот что нашлось по вашему запросу:\n {first_result}', reply_markup=kbd)

                # bot.send_message(message.from_user.id, f'{str(movie)}')
        # bot.send_message(message.from_user.id, 'Выберите дальнейшую опцию', reply_markup=gen_mid_menu())


@bot.callback_query_handler(state=SearchState.n_count, func=lambda callback_query: (callback_query.data == "continue"))
def continue_current_mode(callback_query) -> None:
    """Хэндлер для повторного запуска поиска фильмов по названию"""

    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bot.send_message(callback_query.from_user.id, 'Введите название фильма или сериала')
    bot.set_state(callback_query.from_user.id, SearchState.n_name)




