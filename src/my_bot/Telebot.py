import logging
import os

import telebot

from .ai_logic import get_new_chat
from typing import Dict, Any
from telebot import types
from my_bot import models
from my_bot.models import Task

logger = logging.getLogger(__name__)
logger.info("Bot handlers and AI logic loaded")

token = os.environ.get("TELEGRAM_TOKEN")
if token is None:
    raise ValueError("TELEGRAM_TOKEN is not set in environment variables")
bot = telebot.TeleBot(token)

user_chats: Dict[int, Any] = {}


@bot.message_handler(commands=["clear"])
def clear_history(message: types.Message) -> None:
    if message.from_user is None:
        return
    user_id = message.from_user.id
    db = models.SessionLocal()
    try:
        db.query(Task).filter(Task.user_id == message.from_user.id).delete()
        db.commit()
        user_chats[user_id] = get_new_chat()
        bot.send_message(message.chat.id, "🧹 Your task history has been erased.")

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clear history for user {user_id}: {e}")

        bot.send_message(
            message.chat.id,
            "⚠️ Service is temporarily unavailable. Please try again later.",
        )
    finally:
        db.close()


RANDOM_TASKS = [
    "Read a chapter of Ulysses @Reading",
    "Compliment a stranger @Crazy",
    "Give away some clothes @Karma",
    "Pick up litter in the neighbourhood @Karma",
    "Fix the damn door @HomeSweetHome",
    "Dance party with kids @Kids",
    "Wash the car @Car",
]

HELP = """
/help - list available commands.
/add - add task to list (date + task + @category).
/show, /print - show all tasks added for the specified dates.
/random - add a random task for the date Today."""


@bot.message_handler(commands=["help"])
def help(message: types.Message) -> None:
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add", "todo"])
def add(message: types.Message) -> None:
    if message.from_user is None:
        return
    if message.text is None:
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, "Usage: /add <date> <task> @<category>")
        return

    date = parts[1].lower()
    task_text = parts[2]
    user_id = message.from_user.id

    db = models.SessionLocal()
    try:
        new_task = Task(user_id=user_id, date=date, text=task_text)
        db.add(new_task)
        db.commit()
        bot.send_message(message.chat.id, f"✅ Task added for {date}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding task for {user_id}: {e}")
        bot.send_message(message.chat.id, "⚠️ Error saving task. Please try again.")
    finally:
        db.close()


@bot.message_handler(commands=["random"])
def random_add(message: types.Message) -> None:
    if message.from_user is None:
        return
    user_id = message.from_user.id
    date = "tomorrow"
    task_text = "Learn something new with AI"  # Или любая логика рандома

    db = models.SessionLocal()
    try:
        new_task = Task(user_id=user_id, date=date, text=task_text)
        db.add(new_task)
        db.commit()
        bot.send_message(
            message.chat.id, f"🎲 Random task added for {date}: {task_text}"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error in random task for {user_id}: {e}")
        bot.send_message(message.chat.id, "⚠️ Error creating random task.")
    finally:
        db.close()


@bot.message_handler(commands=["show", "print"])
def show(message: types.Message) -> None:
    if message.from_user is None:
        return
    if message.text is None:
        return

    command = message.text.split()
    dates = [date.lower() for date in command[1:]]
    user_id = message.from_user.id

    db = models.SessionLocal()
    try:
        response = ""
        for date in dates:
            tasks = (
                db.query(Task).filter(Task.user_id == user_id, Task.date == date).all()
            )

            response += f"📅 {date.upper()}:\n"
            if tasks:
                for t in tasks:
                    response += f"- {t.text}\n"
            else:
                response += "No tasks planned.\n"
            response += "\n"

        bot.send_message(message.chat.id, response or "Please specify dates.")
    except Exception as e:
        logger.error(f"Error showing tasks for {user_id}: {e}")
        bot.send_message(message.chat.id, "⚠️ Could not retrieve tasks.")
    finally:
        db.close()


@bot.message_handler(func=lambda message: True)
def handle_gemini_chat(message):
    user_id = message.from_user.id if message.from_user else None

    if not user_id:
        logger.warning("Received a message without a valid user_id")
        return
    try:
        if user_id not in user_chats:
            user_chats[user_id] = get_new_chat()

        chat = user_chats[user_id]

        logger.info(f"User {user_id} wrote: {message.text[:30]}")

        response = chat.send_message(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        logger.error(f"AI Chat Error for user {user_id}: {e}", exc_info=True)

        bot.send_message(
            message.chat.id,
            "⚠️ Sorry, I'm having trouble processing your request right now. Please try again later.",
        )
