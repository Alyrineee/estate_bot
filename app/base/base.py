import estate_bot.app.base.base_keyboards

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart

base = Router()
ADMINS = [
    5253078721,
]


class RegistrationState(StatesGroup):
    phone_number = State()
    email = State()


@base.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую!\nВыбери роль:",
        reply_markup=estate_bot.app.base.base_keyboards.role_choice_keyboard,
    )


@base.callback_query(F.data == "agent")
async def callback_agent(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.phone_number)
    await callback.answer()
    await callback.message.answer(
        "Вы выбрали агента\n\n" "Пожалуйста укажите Ваш номер телефона"
    )


@base.message(RegistrationState.phone_number)
async def state_phone_number(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.email)
    await state.update_data(
        number=message.text,
    )
    await message.answer(
        "Пожалуйста укажите Ваш email\n\n"
        "Если Вы не хотите оставлять свой email, отправьте точку"
    )


@base.message(RegistrationState.email)
async def state_email(message: Message, state: FSMContext):
    await state.update_data(
        email=message.text,
    )
    await message.answer("Регистрация успешна, ожидайте")
    await message.bot.send_message(ADMINS[0], "Новая заявка")
    await state.clear()
