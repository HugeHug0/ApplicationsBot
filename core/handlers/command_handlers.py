from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.keyboards.reply_keyboards import start_application_keyboard
from core.utils import text

router = Router()

@router.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer(text.start_command_message, reply_markup=start_application_keyboard())

