from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
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
        ]
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

def houses_inline_keyboard(data):
    keyboard = InlineKeyboardBuilder()
    for house in data:
        keyboard.add(InlineKeyboardButton(
            text=house[0], callback_data=f"{house[0]}_{house[1]}"
        ))
    return keyboard.adjust(1).as_markup()

