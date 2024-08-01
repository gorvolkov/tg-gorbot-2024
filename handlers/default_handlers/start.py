from telebot.types import Message

from config_data.config import ALL_COMMANDS
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    # commands = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, f"Здравствуйте, {message.from_user.full_name}! "
                          f"Это бот Кинопоиска, который поможет вам сориентироваться в мире кинематографа.\n"
                          f"Я выполняю следующие команды:\n\n"
                          f"/movie_search — поиск фильма/сериала по названию\n"
                          f"/movie_by_rating — поиск фильмов/сериалов по рейтингу\n"
                          f"/low_budget_movie — поиск фильмов/сериалов с низким бюджетом\n"
                          f"/high_budget_movie — поиск фильмов/сериалов с высоким бюджетом\n"
                          f"/history — просмотр истории ваших запросов и поиска фильма/сериала\n")

    # commands = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    # bot.reply_to(message, "\n".join(commands))

