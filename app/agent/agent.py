from urllib3 import request

import estate_bot.app.base.base_keyboards
from estate_bot.app.agent.agent_keyboards import region_inline_keyboard, budget_inline_keyboard, houses_inline_keyboard
from estate_bot.config import ADMINS
from estate_bot.utils.google_api.models import UserCreation, AgentRequest

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

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
async def state_phone_number(callback: CallbackQuery, state: FSMContext):
   await state.set_state(RequestStates.budget)
   await state.update_data(region=callback.data)
   await callback.answer()
   await callback.message.answer(
       "Укажите бюджет клиента:",
        reply_markup = budget_inline_keyboard,
   )


@agent.callback_query(RequestStates.budget)
async def state_phone_number(callback: CallbackQuery, state: FSMContext):
    await state.update_data(budget=callback.data)
    await state.set_state(RequestStates.house)
    await callback.answer()
    await callback.message.answer(
        "Выберите ЖК",
        reply_markup = houses_inline_keyboard(table.get_houses()),
    )


@agent.callback_query(RequestStates.house)
async def state_phone_number(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    await callback.answer()
    await state.update_data(
        house=data[0],
        builder=data[1],
    )
    print(await state.get_data())
    await callback.message.answer("Успешно")
