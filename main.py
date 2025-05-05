import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from handlers import register_handlers

logging.basicConfig(level=config.LOGGING_LEVEL, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Главная асинхронная функция для инициализации и запуска бота.
    """

    logger.info("--- Запуск Бота ---")
    logger.info(
        f"Используется токен: {'***' + config.TELEGRAM_TOKEN[-4:] if config.TELEGRAM_TOKEN else 'Не найден!'}")  # Не логируем токен целиком
    logger.info(f"Путь к модели: {config.MODEL_PATH}")
    logger.info(f"Устройство для модели: {config.DEVICE}")

    dp = Dispatcher()

    register_handlers(dp)

    bot = Bot(
        token=config.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    logger.info("Удаление вебхука (если был) и запуск polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Остановка бота...")

        await bot.session.close()
        logger.info("Бот остановлен.")


# Точка входа в скрипт
if __name__ == "__main__":
    if not config.TELEGRAM_TOKEN:
        logger.critical("Невозможно запустить бота: TELEGRAM_TOKEN не установлен!")
        sys.exit(1)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Получен сигнал завершения. Бот останавливается.")
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка на верхнем уровне: {e}")
