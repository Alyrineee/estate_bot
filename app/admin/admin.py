from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from estate_bot.app.admin.admin_keyboards import (
    houses_inline_keyboard,
    update_houses_keyboard,
)
from estate_bot.app.base.base_keyboards import access_keyboard
from estate_bot.app.keyboards import paginate_inline_keyboard
from estate_bot.utils.google_api.models import AdminManager

admin = Router()
table = AdminManager()


class HouseUpdateStates(StatesGroup):
    house = State()
    builder = State()


@admin.message(Command("view_requests"))
async def cmd_view_request(message: Message):
    await message.answer(
        "Выбери заявку",
        reply_markup=paginate_inline_keyboard(
            table.get_clients(),
            1,
            "viewrequest",
        ),
    )


@admin.callback_query(F.data.startswith("viewrequestpage"))
async def request_paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=paginate_inline_keyboard(
            table.get_clients(),
            int(callback.data.split("#")[1]),
            "viewrequest",
        ),
    )


@admin.callback_query(F.data.startswith("viewrequest"))
async def callback_request_view(callback: CallbackQuery):
    await callback.answer()
    data = table.get_client(callback.data.split("#")[1])
    await callback.message.edit_text(
        f"ФИО: {data[1]}\n"
        f"Номер телефона: {data[2]}\n"
        f"Регион: {data[3]}\n"
        f"Бюджет: {data[4]}\n"
        f"ЖК: {data[5]}\n"
        f"Статус: {data[6]}",
    )


@admin.message(Command("manage_users"))
async def cmd_manage_users(message: Message):
    await message.answer(
        "Выбери пользователя",
        reply_markup=paginate_inline_keyboard(
            table.get_users(),
            1,
            "user",
        ),
    )


@admin.callback_query(F.data.startswith("userpage"))
async def paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=paginate_inline_keyboard(
            table.get_users(),
            int(callback.data.split("#")[1]),
            "user",
        ),
    )


@admin.callback_query(F.data.startswith("user"))
async def callback_user_view(callback: CallbackQuery):
    await callback.answer()
    data = table.get_user(callback.data.split("#")[1])
    await callback.message.edit_text(
        f"ФИО: {data[1]}\n"
        f"Email: {data[2]}\n"
        f"Номер телефона: {data[3]}\n"
        f"Должность: {data[4]}\n"
        f"Cтатус: {data[5]}",
        reply_markup=access_keyboard(
            telegram_id=callback.message.chat.id,
        ),
    )


@admin.message(Command("update_database"))
async def cmd_update_database(message: Message):
    await message.answer(
        "Выбери ЖК",
        reply_markup=houses_inline_keyboard(
            table.get_houses(),
            1,
        ),
    )


@admin.callback_query(F.data.startswith("housepage"))
async def callback_paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=houses_inline_keyboard(
            table.get_houses(),
            int(callback.data.split("#")[1]),
        ),
    )


@admin.callback_query(F.data.startswith("house"))
async def callback_house_view(callback: CallbackQuery):
    await callback.answer()
    data = table.get_house(callback.data.split("#")[1])
    await callback.message.edit_text(
        f"ЖК: {data[1]}\n" f"Застройщик: {data[2]}\n",
        reply_markup=update_houses_keyboard(
            callback.data.split("#")[1],
        ),
    )


@admin.callback_query(F.data == "createhouse")
async def callback_create(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(HouseUpdateStates.house)
    await state.update_data(house_id="")
    await callback.message.answer("Введи название ЖК: ")


@admin.callback_query(F.data.startswith("delete"))
async def callback_delete_house(callback: CallbackQuery):
    await callback.answer()
    table.delete_house(callback.data.split("#")[1])
    await callback.message.answer("Успешно")


@admin.callback_query(F.data.startswith("update"))
async def callback_update_house(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(HouseUpdateStates.house)
    await state.update_data(house_id=callback.data.split("#")[1])
    await callback.message.answer("Введи название ЖК: ")


@admin.message(HouseUpdateStates.house)
async def stare_house(message: Message, state: FSMContext):
    await state.set_state(HouseUpdateStates.builder)
    await state.update_data(house=message.text)
    await message.answer("Введи название застройщика: ")


@admin.message(HouseUpdateStates.builder)
async def state_builder(message: Message, state: FSMContext):
    await state.update_data(builder=message.text)
    data = await state.get_data()
    table.edit_house(
        data["house_id"],
        [
            data["house"],
            data["builder"],
        ],
    )
    await state.clear()
    await message.answer("Успешно изменено✅")
