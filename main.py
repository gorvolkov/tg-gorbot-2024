from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_commands
from database.models import User, create_models
from loader import bot
import handlers

if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_commands(bot)
    bot.infinity_polling()
