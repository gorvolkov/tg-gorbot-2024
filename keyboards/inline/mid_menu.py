from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_mid_menu():
    button_1 = InlineKeyboardButton(text="Продолжить", callback_data="continue")
    button_2 = InlineKeyboardButton(text="Завершить", callback_data="quit")
    button_3 = InlineKeyboardButton(text="В главное меню", callback_data="to_main")

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(button_1, button_2, button_3)
    return keyboard
