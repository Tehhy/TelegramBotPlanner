import logging
import os
import random

import telebot

from .ai_logic import get_new_chat
from typing import Dict, List, Any
from telebot import types

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
    try:
        user_chats[user_id] = get_new_chat()
        bot.send_message(
            message.chat.id, "🧹 Our conversation history has been erased."
        )

    except Exception as e:
        logger.error(f"Failed to clear history for user {user_id}: {e}")

        bot.send_message(
            message.chat.id,
            "⚠️ AI service is temporarily unavailable. Please try again later.",
        )


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

tasks: Dict[str, List[str]] = {}


def add_todo(date: str, task: str) -> None:
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=["help"])
def help(message: types.Message) -> None:
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=["add", "todo"])
def add(message: types.Message) -> None:
    if message.text is None:
        return
    try:
        command = message.text.split(maxsplit=1)
        if len(command) < 2:
            bot.send_message(
                message.chat.id,
                "Invalid command format. Use: /add <date> <task> @<category>",
            )
            return
        date = command[1].split()[0].lower()
        task_with_category = command[1].split(maxsplit=1)[1]
        if "@" in task_with_category:
            task, category = task_with_category.split("@", maxsplit=1)
            task = task.strip()
            category = "@" + category.strip()
        else:
            task = task_with_category.strip()
            category = ""
        add_todo(date, task + " " + category)
        bot.send_message(
            message.chat.id, f"Task '{task} {category}' added on date {date}"
        )
    except IndexError:
        bot.send_message(
            message.chat.id,
            "Invalid command format. Use: /add <date> <task> @<category>",
        )


@bot.message_handler(commands=["random"])
def random_add(message: types.Message) -> None:
    date = "today"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    bot.send_message(message.chat.id, f"Task '{task}' added on date {date}")


@bot.message_handler(commands=["show", "print"])
def show(message: types.Message) -> None:
    if message.text is None:  # Исправление для Mypy
        return
    command = message.text.split()
    if len(command) < 2:
        bot.send_message(
            message.chat.id, "Invalid command format. Use: /show <date1> <date2> ..."
        )
        return
    dates = [date.lower() for date in command[1:]]
    result = ""
    for date in dates:
        if date in tasks:
            result += date.upper() + "\n"
            for task in tasks[date]:
                result += f"[ ] {task}\n"
        else:
            result += f"There are no tasks for date {date}\n"
    bot.send_message(message.chat.id, result)


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
