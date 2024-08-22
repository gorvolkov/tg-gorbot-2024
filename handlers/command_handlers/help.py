from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    """Обработчик команды /help"""
    bot.send_message(message.from_user.id, "Я не уверен, нужна ли тут эта команда")
