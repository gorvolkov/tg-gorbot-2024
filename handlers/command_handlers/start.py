from telebot.types import Message
from sqlite3 import IntegrityError


from loader import bot
from keyboards.inline.main_menu import gen_main_menu
from database.models import User


@bot.message_handler(commands=["start"])
def greeting(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        existing_user = User.get(User.user_id == user_id)
        bot.reply_to(message, f"Рад вас снова видеть, {first_name}!\n"
                              f"Выберите направление поиска", reply_markup=gen_main_menu())
    except User.DoesNotExist:
        try:
            User.create(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            bot.reply_to(message, f"Здравствуйте, {first_name}!\n"
                              f"Я бот Кинопоиска, который поможет вам сориентироваться в мире кинематографа.\n"
                              f"Для продолжения выберите направление поиска", reply_markup=gen_main_menu())
        except IntegrityError:
            bot.reply_to(message, f"Ошибка при создании пользователя.")



