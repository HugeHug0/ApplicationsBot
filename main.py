import asyncio
import logging
import os
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.settings import settings
from core.handlers import basic_handlers, command_handlers


async def start_bot(bot: Bot, dp: Dispatcher):
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def start_web():
    async def handle(request):
        return web.Response(text="Bot is running!")

    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    return runner


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_router(basic_handlers.router)
    dp.include_router(command_handlers.router)

    runner = await start_web()

    # Запускаем бот и сервер параллельно
    bot_task = asyncio.create_task(start_bot(bot, dp))

    try:
        await bot_task
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
