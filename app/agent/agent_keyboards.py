from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

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
                text="20-35 млн",
                callback_data="around2",
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
