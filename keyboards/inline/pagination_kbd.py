from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_pagination_kbd(page: int, count: int) -> InlineKeyboardMarkup:

    button_1 = InlineKeyboardButton(text=f'<-', callback_data=f"pagination_backward_{page}_{count}")
    button_2 = InlineKeyboardButton(text=f"{page}/{count}", callback_data="_")
    button_3 = InlineKeyboardButton(text=f'->', callback_data=f"pagination_forward_{page}_{count}")
    button_4 = InlineKeyboardButton(text='Новый запрос', callback_data='pagination_quit')

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard
