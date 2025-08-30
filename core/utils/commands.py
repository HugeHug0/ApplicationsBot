from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def set_commands(bot: Bot):  # Регистрация команд
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
