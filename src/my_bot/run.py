import os

from dotenv import load_dotenv

load_dotenv()

import logging  # noqa: E402

from my_bot.Telebot import bot  # noqa: E402

from my_bot.models import init_db  # noqa: E402


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "bot.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize database: {e}", exc_info=True)
        exit(1)

    logger.info("Starting the bot polling...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.critical(f"Critical crash: {e}", exc_info=True)
