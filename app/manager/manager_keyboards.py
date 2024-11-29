from math import ceil

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def clients_inline_keyboard(data, page):
    keyboard = InlineKeyboardBuilder()
    if page > ceil(len(data) / 5):
        page = ceil(len(data) / 5)

    left, right = (page - 1) * 5, min(len(data), (page - 1) * 5 + 5)
    for request in data[left:right]:
        keyboard.add(
            InlineKeyboardButton(
                text=request[1],
                callback_data=f"request#{request[0]}",
            )
        )

    bottom_buttons = []
    if page != 1:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"rpage#{page-1}",
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
                callback_data=f"rpage#{page+1}",
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


def client_accept_keyboard(client_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Клиент уникален",
                    callback_data=f"caccept#{client_id}",
                ),
                InlineKeyboardButton(
                    text="Клиент не уникален",
                    callback_data=f"cdecline#{client_id}",
                ),
            ]
        ]
    )
