from math import ceil

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def houses_inline_keyboard(data, page):
    keyboard = InlineKeyboardBuilder()
    if page > ceil(len(data) / 5):
        page = ceil(len(data) / 5)

    left, right = (page - 1) * 5, min(len(data), (page - 1) * 5 + 5)
    for house in data[left:right]:
        keyboard.add(
            InlineKeyboardButton(
                text=house[1],
                callback_data=f"house#{house[0]}",
            )
        )

    bottom_buttons = []
    if page != 1:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"hpage#{page-1}",
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
                callback_data=f"housepage#{page+1}",
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
    keyboard.row(
        InlineKeyboardButton(text="Создать ЖК➕", callback_data="createhouse")
    )
    return keyboard.as_markup()


def update_houses_keyboard(house_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Обновить данные",
                    callback_data=f"update#{house_id}",
                ),
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=f"delete#{house_id}",
                ),
            ],
        ]
    )
