from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from estate_bot.app.manager.manager_keyboards import (
    client_accept_keyboard,
    clients_inline_keyboard,
)
from estate_bot.utils.google_api.models import ClientManager

manager = Router()
table = ClientManager()


@manager.message(Command("check_requests"))
async def check_requests(message: Message):
    await message.answer(
        "Выберите заявку",
        reply_markup=clients_inline_keyboard(table.get_clients(), 1),
    )


@manager.callback_query(F.data.startswith("rpage"))
async def paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=clients_inline_keyboard(
            table.get_clients(),
            int(callback.data.split("#")[1]),
        ),
    )


@manager.callback_query(F.data.startswith("request"))
async def callback_request(callback: CallbackQuery):
    await callback.answer()
    client = table.get_client(callback.data.split("#")[1])
    await callback.message.edit_text(
        f"Клиент: {client[1]}\n"
        f"Номер телефона: {client[2]}\n"
        f"Регион: {client[3]}\n"
        f"Бюджет: {client[4]}\n"
        f"ЖК: {client[5]}\n",
        reply_markup=client_accept_keyboard(client[0]),
    )


@manager.callback_query(F.data.startswith("caccept"))
async def callback_client_accept(callback: CallbackQuery):
    await callback.answer()
    table.edit_status(
        int(callback.data.split("#")[1]),
        "Клиент уникален",
    )
    await callback.message.edit_text("Успешно")


@manager.callback_query(F.data.startswith("cdecline"))
async def callback_client_decline(callback: CallbackQuery):
    await callback.answer()
    table.edit_status(
        int(callback.data.split("#")[1]),
        "Клиент не уникален",
    )
    await callback.message.edit_text("Успешно")