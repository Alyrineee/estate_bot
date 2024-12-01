from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
import estate_bot.app.base.base_keyboards
from estate_bot.config import ADMINS
from estate_bot.utils.google_api.models import UserCreation

base = Router()
table = UserCreation()


class RegistrationState(StatesGroup):
    phone_number = State()
    full_name = State()
    email = State()


@base.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Перед началом работы, пожалуйста, выберите вашу роль:\n"
        "- 🕵️‍♂️ Агент (являетесь представителем компании или клиентом)\n"
        "- ✍️ Оформитель (занимаетесь документами)\n\n"
        "После выбора роли нам понадобятся ваши данные, чтобы начать",
        reply_markup=estate_bot.app.base.base_keyboards.role_choice_keyboard,
    )


@base.callback_query(F.data == "agent")
async def callback_agent(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.phone_number)
    await callback.answer()
    await state.update_data(
        type="Агент",
    )
    await callback.message.answer(
        "Вы выбрали агента\n\n"
        "Пожалуйста нажмите на кнопку чтобы поделиться номером телефона",
        reply_markup=estate_bot.app.base.base_keyboards.contact_keyboard,
    )


@base.callback_query(F.data == "manager")
async def callback_manager(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationState.phone_number)
    await callback.answer()
    await state.update_data(
        type="Оформитель",
    )
    await callback.message.answer(
        "Вы выбрали оформителя\n\n"
        "Пожалуйста нажмите на кнопку чтобы поделиться номером телефона",
        reply_markup=estate_bot.app.base.base_keyboards.contact_keyboard,
    )


@base.message(RegistrationState.phone_number, F.contact)
async def state_phone_number(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.full_name)
    await state.update_data(
        number=message.contact.phone_number,
    )
    await message.answer(
        "Как Вас зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )


@base.message(RegistrationState.full_name)
async def state_full_name(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.email)
    await state.update_data(
        full_name=message.text,
    )
    await message.answer(
        "Пожалуйста укажите Ваш email\n\n"
        "Если Вы не хотите оставлять свой email, отправьте точку",
    )


@base.message(RegistrationState.email)
async def state_email(message: Message, state: FSMContext):
    await state.update_data(
        email=message.text,
    )
    data = await state.get_data()
    await message.answer("Регистрация успешна, ожидайте")
    for admin_id in ADMINS:
        await message.bot.send_message(
            admin_id,
            f"Новая заявка⚠️\n\n"
            f"ФИО: {data['full_name']}\n"
            f"Email: {data['email']}\n"
            f"Должность: {data['type']}",
            reply_markup=estate_bot.app.base.base_keyboards.access_keyboard(
                telegram_id=message.chat.id,
            ),
        )

    table.request_creation(
        data=[
            message.chat.id,
            data["full_name"],
            data["email"],
            data["number"],
            data["type"],
            "Ожидает активации",
        ]
    )
    await state.clear()


@base.callback_query(F.data.startswith("accept"))
async def callback_user_accept(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.data.replace("accept#", "")
    table.request_accept(
        user_id,
        "Активирован",
    )
    await callback.bot.send_message(user_id, "Вашу заявку подтвердили✅")
    await callback.message.edit_text("Пользователь активирован✅")


@base.callback_query(F.data.startswith("decline"))
async def callback_user_decline(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.data.replace("decline#", "")
    table.request_accept(
        user_id,
        "Дективирован",
    )
    await callback.bot.send_message(user_id, "Вашу заявку отклонили❌")
    await callback.message.edit_text("Пользователь деактивирован❌")
