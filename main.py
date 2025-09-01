import asyncio
import logging
import os
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.settings import settings
from core.handlers import basic_handlers, command_handlers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_router(basic_handlers.router)
    dp.include_router(command_handlers.router)

    # -------------------
    # минимальный веб-сервер для Render
    async def handle(request):
        return web.Response(text="Bot is running!")

    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    # -------------------

    # запускаем параллельно polling и web-сервер
    polling_task = asyncio.create_task(dp.start_polling(bot))
    try:
        await polling_task
    finally:
        await bot.session.close()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())