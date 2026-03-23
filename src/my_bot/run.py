import logging
import os

from my_bot.Telebot import bot

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
    logger.info("Starting the application...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.critical(f"Critical crash: {e}", exc_info=True)
