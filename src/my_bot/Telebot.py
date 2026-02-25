import os
import telebot
import random

token = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token)

RANDOM_TASKS = ["Read a chapter of Ulysses @Reading", "Compliment a stranger @Crazy",
                "Give away some clothes @Karma", "Pick up litter in the neighbourhood @Karma",
                "Fix the damn door @HomeSweetHome", "Dance party with kids @Kids", "Wash the car @Car"]

HELP = """
/help - list available commands.
/add - add task to list (date + task + @category).
/show, /print - show all tasks added for the specified dates.
/random - add a random task for the date Today."""

tasks = {}

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add", "todo"])
def add(message):
    try:
        command = message.text.split(maxsplit=1)
        if len(command) < 2:
            bot.send_message(message.chat.id, "Invalid command format. Use: /add <date> <task> @<category>")
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
        bot.send_message(message.chat.id, f"Task '{task} {category}' added on date {date}")
    except IndexError:
        bot.send_message(message.chat.id, "Invalid command format. Use: /add <date> <task> @<category>")

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "today"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    bot.send_message(message.chat.id, f"Task '{task}' added on date {date}")

@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split()
    if len(command) < 2:
        bot.send_message(message.chat.id, "Invalid command format. Use: /show <date1> <date2> ...")
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

