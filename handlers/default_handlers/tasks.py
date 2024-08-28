
from typing import List
from loader import bot
from telebot.types import Message

from models import Task, User


@bot.message_handler(state="*", commands=["history"])
def handle_tasks(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    tasks: List[Task] = user.tasks.order_by(-Task.task_id).limit(10)

    result = []
    result.extend(map(str, reversed(tasks)))

    if not result:
        bot.send_message(message.from_user.id, "У вас ещё нет записей")
        return

    #result.append("\nВведите номер задачи, чтобы изменить её статус.")
    bot.send_message(message.from_user.id, "\n".join(result))
