from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from estate_bot.app.agent.agent_keyboards import (
    budget_inline_keyboard,
    houses_inline_keyboard,
    region_inline_keyboard, agent_access_keyboard,
)
from estate_bot.utils.google_api.models import AgentRequest

agent = Router()
table = AgentRequest()


class RequestStates(StatesGroup):
    full_name = State()
    phone_number = State()
    region = State()
    budget = State()
    house = State()


@agent.message(Command("new_request"))
async def cmd_new_request(message: Message, state: FSMContext):
    await state.set_state(RequestStates.full_name)
    await message.answer("Укажите ФИО клиента:")


@agent.message(RequestStates.full_name)
async def state_full_name(message: Message, state: FSMContext):
    await state.set_state(RequestStates.phone_number)
    await state.update_data(full_name=message.text)
    await message.answer("Укажите номер телефона клиента:")


@agent.message(RequestStates.phone_number)
async def state_phone_number(message: Message, state: FSMContext):
    await state.set_state(RequestStates.region)
    await state.update_data(phone_number=message.text)
    await message.answer(
        "Укажите регион клиента:",
        reply_markup=region_inline_keyboard,
    )


@agent.callback_query(RequestStates.region)
async def state_region(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RequestStates.budget)
    region = "Москва"
    if callback.data == "Other":
        region = "Другой регион"

    await state.update_data(region=region)
    await callback.answer()
    await callback.message.answer(
        "Укажите бюджет клиента:",
        reply_markup=budget_inline_keyboard,
    )


@agent.callback_query(RequestStates.budget)
async def state_budget(callback: CallbackQuery, state: FSMContext):
    page = await state.get_data()
    budget = {
        "less": "до 15 млн",
        "around": "15-20 млн",
        "more": "более 35 млн",
    }
    await state.update_data(budget=budget[callback.data])
    await state.set_state(RequestStates.house)
    await callback.answer()
    await callback.message.answer(
        "Выберите ЖК",
        reply_markup=houses_inline_keyboard(
            table.get_houses(),
            page.get("current_page", 1),
        ),
    )


@agent.callback_query(F.data.startswith("page"))
async def paginate_page(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=houses_inline_keyboard(
            table.get_houses(),
            int(callback.data.split("#")[1]),
        ),
    )


@agent.callback_query(RequestStates.house)
async def state_house(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data.split("_")
    await callback.answer()
    await state.set_state(None)
    await state.update_data(
        house=callback_data[0],
        builder=callback_data[1],
    )
    data = await state.get_data()
    await callback.message.answer(
        "Подтвердите заявку⚠️\n\n"
        f"Имя: {data["full_name"]}\n"
        f"Телефон: {data["phone_number"]}\n"
        f"Регион: {data["region"]}\n"
        f"Бюджет: {data["budget"]}\n"
        f"ЖК: {data["house"]}\n"
        f"Застройщик: {data["builder"]}\n",
        reply_markup=agent_access_keyboard,
    )


@agent.callback_query(F.data == "agent_accept")
async def callback_agent_accept(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    table.create_agent_request(
        [
            data["full_name"],
            data["phone_number"],
            data["region"],
            data["budget"],
            data["house"],
            "Ожидает ответа",
        ],
    )
    await state.clear()
    await callback.message.edit_text("Заявка успешно создана✅")


@agent.callback_query(F.data == "agent_decline")
async def callback_agent_accept(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("Заявка удалена❌")