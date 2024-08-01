from telebot.types import Message
from config_data.config import ALL_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in ALL_COMMANDS]
    bot.reply_to(message, "\n".join(text))
