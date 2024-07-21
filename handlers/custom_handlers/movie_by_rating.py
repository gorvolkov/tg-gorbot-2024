from keyboards.reply.contact import request_contact
from loader import bot
from states.movie_params import MovieInfoState
from telebot.types import Message


@bot.message_handler(commands=['movie_by_rating'])
def get_genre(message: Message) -> None:
    bot.set_state(message.from_user.id, MovieInfoState.genre, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}! Введите интересующий вас жанр фильмов')

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


@bot.message_handler(state=MovieInfoState.count)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number

            text = (f'Спасибо за предоставленную информацию, {message.from_user.username}.\n'
                    f'Ваши данные:\n'
                    f'1. Имя: {data['name']}\n'
                    f'2. Возраст: {data['age']}\n'
                    f'3. Страна проживания: {data['country']}\n'
                    f'4. Город проживания: {data['city']}\n'
                    f'5. Номер телефона: {data['phone_number']}\n\n'
                    f'Это был запуск тестового скрипта для проверки работы машины состояний')
            bot.send_message(message.from_user.id, text)



    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию, нажмите на кнопку')

