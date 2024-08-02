from telebot.types import Message
from config_data.config import ALL_COMMANDS
from loader import bot
from keyboards.inline.main_menu import gen_main_menu


@bot.message_handler(commands=["start"])
def greeting(message: Message):
    # Приветствие пользователя, обзор функций бота, отправляем пользователю клавиатуру для выбора направления поиска

    # commands = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    # commands = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    # bot.reply_to(message, "\n".join(commands))

    bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.full_name}! "
                          f"Это бот Кинопоиска, который поможет вам сориентироваться в мире кинематографа.\n"
                          f"Я выполняю следующие команды:\n\n"
                          f"/movie_search — поиск фильма/сериала по названию\n"
                          f"/movie_by_rating — поиск фильмов/сериалов по рейтингу\n"
                          f"/low_budget_movie — поиск фильмов/сериалов с низким бюджетом\n"
                          f"/high_budget_movie — поиск фильмов/сериалов с высоким бюджетом\n"
                          f"/history — просмотр истории ваших запросов и поиска фильма/сериала\n\n"
                                           f"Выберите направление поиска", reply_markup=gen_main_menu())


# @bot.message_handler(state=UserState.start_state)
# def main_menu(message: Message):
#     bot.send_message(message.from_user.id, )


