import time
from loader import bot
from typing import List, Dict
from states.dialog_state import UserDialogState
from telebot.types import Message
from keyboards.reply.menu_keyboard import menu
from keyboards.reply.menu_keyboard import get_ticket
from keyboards.reply.menu_keyboard import cancel
from api.get_low_request import low_request
from api.get_high_request import high_request
from api.get_custom_daydata import custom_daydata_request
import datetime
from database.models import Task, User


def save_to_history(message):
    today = datetime.datetime.now()
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_task"] = {"user_id": message.from_user.id}
        data["new_task"]["title"] = message.text
        data["new_task"]["due_date"] = today
    new_task = Task(**data["new_task"])
    new_task.save()
    bot.send_message(message.from_user.id, f"Добавлена запись в историю:\n{new_task}")


def menu_clicked(message):
    variants = "Low", "High", "дату"
    return message.text.endswith(variants)


#@bot.message_handler(func=menu_clicked) # TODO после добавления этой строки перестал работать
@bot.message_handler(state=UserDialogState.start_dialog) # Ловим состояние
#@bot.message_handler(func=menu_clicked)#, state=UserDialogState.start_dialog)
def handle_start_dialog(message: Message):
    if message.text == 'Самый дешевый - Low':
        save_to_history(message)
        bot.send_message(message.from_user.id, 'Выбран Low', reply_markup=get_ticket())
        bot.set_state(message.from_user.id, UserDialogState.state_low)
    elif message.text == 'Самый популярный - High':
        save_to_history(message)
        bot.send_message(message.from_user.id, 'Выбран High', reply_markup=get_ticket())
        bot.set_state(message.from_user.id, UserDialogState.state_high)
    elif message.text == 'Изменить дату':
        bot.send_message(message.from_user.id, 'Выбран Custom')
        bot.send_message(message.from_user.id, 'Введите дату в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, UserDialogState.state_custom)
    else:
        bot.set_state(message.from_user.id, state=None)


@bot.message_handler(state=UserDialogState.state_low)
def handle_state_low(message: Message):
    bot.send_message(message.from_user.id, 'Сейчас в Low')
    bot.send_message(message.from_user.id, 'Самый дешевый билет Сочи -> Белград')
    bot.send_message(message.from_user.id, low_request())
    bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog)


@bot.message_handler(state=UserDialogState.state_high)
def handle_state_high(message: Message):
    bot.send_message(message.from_user.id, 'Сейчас в High')
    bot.send_message(message.from_user.id, 'Самый популярный билет Сочи -> Белград')
    bot.send_message(message.from_user.id, high_request())
    bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog)


@bot.message_handler(state=UserDialogState.state_custom)
def handle_state_custom(message: Message):
    try:
        struct = time.strptime(message.text, '%Y-%m-%d')
        valid_date = time.strftime('%Y-%m-%d', struct)
        bot.send_message(message.from_user.id, 'Сейчас посмотрим')

    except ValueError:
        bot.send_message(message.from_user.id, 'Неверная дата, попробуй еще раз', reply_markup=cancel())
        if message.text == 'Отмена':
            bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
            bot.set_state(message.from_user.id, UserDialogState.start_dialog)
    else:
        message.text = 'Кастомная дата: ' + message.text
        save_to_history(message)
        bot.send_message(message.from_user.id, 'Сейчас в Custom')
        bot.send_message(message.from_user.id, 'Самый дешевый билет Сочи -> Белград на выбранный день')
        bot.send_message(message.from_user.id, custom_daydata_request(valid_date))
        bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
        bot.set_state(message.from_user.id, UserDialogState.start_dialog)




