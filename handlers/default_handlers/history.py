
from typing import List
from loader import bot
from telebot.types import Message
from states.dialog_state import UserDialogState
from database.models import Task, User
from keyboards.reply.menu_keyboard import menu


@bot.message_handler(commands=["history"], state="*")
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

    bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog)
