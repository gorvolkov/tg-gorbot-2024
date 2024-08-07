from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_pagination_kbd(curr_page: int, from_pages: int ) -> InlineKeyboardMarkup:
    left_button = InlineKeyboardButton("←", callback_data="to_left_page")
    page_button = InlineKeyboardButton(f"{str(curr_page)}/{str(from_pages)}", callback_data=None)
    right_button = InlineKeyboardButton("→", callback_data="to_right_page")
    to_main_menu_button = InlineKeyboardButton("В главное меню", callback_data="from_hist_to_main")

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(left_button, page_button, right_button, to_main_menu_button)
    return keyboard
