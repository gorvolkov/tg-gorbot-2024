from loader import bot
import handlers
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_commands

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_commands(bot)
    # bot.polling(none_stop=True, timeout=123)
    bot.infinity_polling()
