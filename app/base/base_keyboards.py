from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
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
            InlineKeyboardButton(
                text="Оформитель",
                callback_data="manager",
            ),
        ],
    ],
)

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Поделиться контактом",
                input_field_placeholder="Нажмите на кнопку",
                request_contact=True,
                resize_keyboard=True,
            )
        ],
    ]
)


def access_keyboard(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Активировать✅",
                    callback_data=f"accept#{telegram_id}",
                ),
                InlineKeyboardButton(
                    text="Деактивировать❌",
                    callback_data=f"decline#{telegram_id}",
                ),
            ],
        ],
    )
