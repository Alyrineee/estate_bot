from math import ceil

from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def paginate_inline_keyboard(data, page, callback_data):
    keyboard = InlineKeyboardBuilder()
    if page > ceil(len(data) / 5):
        page = ceil(len(data) / 5)
    left, right = (page - 1) * 5, min(len(data), (page - 1) * 5 + 5)
    for info in data[left:right]:
        keyboard.add(
            InlineKeyboardButton(
                text=info[1],
                callback_data=f"{callback_data}#{info[0]}",
            )
        )

    bottom_buttons = []
    if page > 1:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"{callback_data}page#{page-1}",
            )
        )
    else:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="❌",
                callback_data="end",
            )
        )

    bottom_buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{ceil(len(data)/5)}",
            callback_data="amount_of_pages",
        )
    )

    if page != ceil(len(data) / 5):
        bottom_buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"{callback_data}page#{page+1}",
            )
        )
    else:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="❌",
                callback_data="end",
            )
        )

    keyboard = keyboard.adjust(1)
    keyboard.row(*bottom_buttons)
    return keyboard.as_markup()
