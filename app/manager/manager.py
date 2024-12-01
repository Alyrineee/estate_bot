from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from estate_bot.app.keyboards import paginate_inline_keyboard
from estate_bot.app.manager.manager_keyboards import (
    client_accept_keyboard,
)
from estate_bot.utils.google_api.models import ClientManager

manager = Router()
table = ClientManager()


class HousesBuilderStates(StatesGroup):
    houses = State()
    builders = State()


@manager.message(Command("check_requests"))
async def cmd_check_requests(message: Message):
    await message.answer(
        "Выберите заявку",
        reply_markup=paginate_inline_keyboard(
            table.get_clients(),
            1,
            "request",
        ),
    )


@manager.callback_query(F.data.startswith("requestpage"))
async def callback_paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=paginate_inline_keyboard(
            table.get_clients(),
            int(callback.data.split("#")[1]),
            "request",
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
async def callback_client_accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(row_id=callback.data.split("#")[1])
    await state.set_state(HousesBuilderStates.houses)
    await callback.message.edit_text("Введите ЖК через запятую")


@manager.callback_query(F.data.startswith("cdecline"))
async def callback_client_decline(callback: CallbackQuery):
    await callback.answer()
    agent_id = table.get_client(callback.data.split("#")[1])[7]
    await callback.bot.send_message(
        agent_id,
        "Клиент не уникален.\n\n"
        "Повторная заявка на данного клиента не требуется.",
    )
    table.edit_status(
        int(callback.data.split("#")[1]),
        "Клиент не уникален",
    )
    await callback.message.edit_text("Успешно")


@manager.message(HousesBuilderStates.houses)
async def state_houses(message: Message, state: FSMContext):
    await state.update_data(houses=message.text)
    await state.set_state(HousesBuilderStates.builders)
    await message.answer("Введите застройщиков через запятую")


@manager.message(HousesBuilderStates.builders)
async def state_builders(message: Message, state: FSMContext):
    await state.update_data(builders=message.text)
    await state.set_state(HousesBuilderStates.builders)
    data = await state.get_data()
    agent_id = table.get_client(data["row_id"])[7]
    table.edit_status(
        int(data["row_id"]),
        "Клиент уникален",
    )
    await message.bot.send_message(
        agent_id,
        f'Клиент уникален для следующих ЖК: {data["houses"]}',
    )

    await message.answer("Успешно✅")
    await state.clear()
