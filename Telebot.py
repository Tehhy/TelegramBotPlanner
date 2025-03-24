import os

import telebot
import random

token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)

RANDOM_TASKS = ["Прочитать главу Божественной комедии @Литература", "Написать письмо Гвидо @Друзья", "Покормить детей @Семья", "Помыть машину @Автомобиль"]

HELP = """
/help - вывести список доступных команд.
/add - добавить задачу в список (дата + задача + категория).
/show - напечатать все добавленные задачи на указанные даты.
/random - добавить случайную задачу на дату Сегодня."""

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
            bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /add <дата> <задача> @<категория>")
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
        bot.send_message(message.chat.id, f"Задача '{task} {category}' добавлена на дату {date}")
    except IndexError:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /add <дата> <задача> @<категория>")

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    bot.send_message(message.chat.id, f"Задача '{task}' добавлена на дату {date}")

@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split()
    if len(command) < 2:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /show <дата1> <дата2> ...")
        return
    dates = [date.lower() for date in command[1:]]
    result = ""
    for date in dates:
        if date in tasks:
            result += date.upper() + "\n"
            for task in tasks[date]:
                result += f"[ ] {task}\n"
        else:
            result += f"Задач на дату {date} нет\n"
    bot.send_message(message.chat.id, result)

bot.polling(none_stop=True)