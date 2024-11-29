from math import ceil

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

region_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Москва",
                callback_data="Moscow",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Другой регион",
                callback_data="Other",
            ),
        ],
    ],
)

budget_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="до 15 млн",
                callback_data="less",
            ),
        ],
        [
            InlineKeyboardButton(
                text="15-20 млн",
                callback_data="around",
            ),
        ],
        [
            InlineKeyboardButton(
                text="до 35 млн",
                callback_data="more",
            ),
        ],
    ],
)


def houses_inline_keyboard(data, page):
    keyboard = InlineKeyboardBuilder()
    if page > ceil(len(data) / 5):
        page = ceil(len(data) / 5)

    left, right = (page - 1) * 5, min(len(data), (page - 1) * 5 + 5)
    for house in data[left:right]:
        keyboard.add(
            InlineKeyboardButton(
                text=house[0],
                callback_data=f"{house[0]}_{house[1]}",
            )
        )

    bottom_buttons = []
    if page != 1:
        bottom_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"page#{page-1}",
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
                callback_data=f"page#{page+1}",
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


agent_access_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Подтвердить✅",
                callback_data="agent_accept",
            ),
            InlineKeyboardButton(
                text="Отмена❌",
                callback_data="agent_decline",
            ),
        ]
    ]
)
