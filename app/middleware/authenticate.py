from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from config import ADMINS
from utils.google_api.models import Authenticate

table = Authenticate()


class AuthenticateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if event.text == "/start":
            if table.authenticate(event.chat.id, "base"):
                return await event.answer("Ты уже зарегистрирован")
        elif event.text == "/new_request":
            if table.authenticate(event.chat.id, "agent"):
                return await event.answer("Недостаточно прав")
        elif event.text == "/check_requests":
            if table.authenticate(event.chat.id, "manager"):
                return await event.answer("Недостаточно прав")
        elif (
            event.text == "/update_database"
            or event.text == "/manage_users"
            or event.text == "/view_requests"
        ):
            if not (str(event.chat.id) in ADMINS):
                return await event.answer("Недостаточно прав")

        return await handler(event, data)
