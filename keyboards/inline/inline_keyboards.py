from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import GENRES_LIST, MAIN_MENU
from keyboa import Keyboa


def main_menu_kbd() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""

    keyboard = Keyboa(items=MAIN_MENU, items_in_row=2).keyboard
    return keyboard


def genres_kbd() -> InlineKeyboardMarkup:
    """Клавиатура с жанрами"""

    keyboard = Keyboa(
        items=GENRES_LIST,
        items_in_row=3,
        copy_text_to_callback=True,
        front_marker="genre_",
    ).keyboard
    return keyboard


def pagination_kbd(page: int, count: int) -> InlineKeyboardMarkup:
    """Клавиатура работы с полученной выборкой фильмов.
    Вторым рядом кнопок реализованы опции нового поиска по выбранному сценарию, завершения работы с ботом или возврата в главное меню
    """

    button_1 = InlineKeyboardButton(
        text=f"<-", callback_data=f"pagination_backward_{page}_{count}"
    )
    button_2 = InlineKeyboardButton(text=f"{page}/{count}", callback_data="_")
    button_3 = InlineKeyboardButton(
        text=f"->", callback_data=f"pagination_forward_{page}_{count}"
    )
    button_4 = InlineKeyboardButton(text="Продолжить", callback_data="continue")
    button_5 = InlineKeyboardButton(text="Завершить", callback_data="quit")
    button_6 = InlineKeyboardButton(text="В главное меню", callback_data="to_main")

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return keyboard
