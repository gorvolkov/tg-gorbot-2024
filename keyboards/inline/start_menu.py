from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot


def gen_markup():
    # Создаём объекты кнопок.
    button_1 = InlineKeyboardButton(text="Поиск по названию", callback_data="movie_by_title")
    button_2 = InlineKeyboardButton(text="Поиск по рейтингу", callback_data="movies_by_rating")
    button_3 = InlineKeyboardButton(text="Фильмы с высоким бюджетом", callback_data="high_budget_movies")
    button_4 = InlineKeyboardButton(text="Фильмы с низким бюджетом", callback_data="low_budget_movies")
    button_5 = InlineKeyboardButton(text="Вывести историю запросов", callback_data="low_budget_movies")
    button_6 = InlineKeyboardButton(text="Завершить", callback_data="low_budget_movies")


    # Создаём объект клавиатуры, добавляя в него кнопки.
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard

bot = TeleBot(
    "7469358742:AAGtcAONz-zOdBK3cSw46i70aQTS8PTb_as"
)  # Токен, полученный от BotFather.

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.from_user.id,
        "Какое животное тебе нравится больше?",
        reply_markup=gen_markup(),  # Отправляем клавиатуру.
    )

@bot.callback_query_handler(
    func=lambda callback_query: (
        callback_query.data  # Обращаемся к callback_data, указанной при создании кнопки.
        == "dog"
    )
)
def dog_answer(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    # Отправляем сообщение пользователю.
    bot.send_message(
        callback_query.from_user.id,
        "Я тоже люблю собак, они так мило машут хвостиком!",
    )

@bot.callback_query_handler(
    func=lambda callback_query: (
        callback_query.data  # Обращаемся к callback_data, указанной при создании кнопки.
        == "cat"
    )
)
def cat_answer(callback_query):
    # Удаляем клавиатуру.
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    # Отправляем сообщение пользователю.
    bot.send_message(
        callback_query.from_user.id,
        "Я тоже люблю кошек, они так умилительно мурлыкают!",
    )

bot.infinity_polling()