from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

role_choice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Агент",
                callback_data="agent",
            ),
        ],
        [
            InlineKeyboardButton(text="Оформитель", callback_data="manager"),
        ],
    ],
)

access_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Одобрить✅",
                callback_data="confirm",
            ),
        ],
    ],
)
