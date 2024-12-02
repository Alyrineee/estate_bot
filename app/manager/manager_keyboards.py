from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def client_accept_keyboard(client_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Клиент уникален",
                    callback_data=f"caccept#{client_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Клиент не уникален",
                    callback_data=f"cdecline#{client_id}",
                ),
            ],
        ]
    )
