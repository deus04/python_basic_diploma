import datetime
import time
import os
from loader import bot
from states.dialog_state import UserDialogState
from telebot.types import Message
from keyboards.reply.menu_keyboard import menu
from keyboards.reply.menu_keyboard import get_ticket
from keyboards.reply.menu_keyboard import cancel
from utils.misc.get_low_request import low_request
from utils.misc.get_high_request import high_request
from utils.misc.get_custom_daydata import custom_daydata_request


@bot.message_handler(state=UserDialogState.start_dialog) # Ловим состояние
def handle_start_dialog(message: Message):
    if message.text == 'Самый дешевый - Low':
        bot.send_message(message.from_user.id, 'Выбран Low', reply_markup=get_ticket())
        bot.set_state(message.from_user.id, UserDialogState.state_low)
    elif message.text == 'Самый популярный - High':
        bot.send_message(message.from_user.id, 'Выбран High', reply_markup=get_ticket())
        bot.set_state(message.from_user.id, UserDialogState.state_high)
    elif message.text == 'Изменить дату':
        bot.send_message(message.from_user.id, 'Выбран Custom')
        bot.send_message(message.from_user.id, 'Введите дату в формате YYYY-MM-DD')
        bot.set_state(message.from_user.id, UserDialogState.state_custom)


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
        bot.send_message(message.from_user.id, 'Сейчас в Custom')
        bot.send_message(message.from_user.id, 'Самый дешевый билет Сочи -> Белград на выбранный день')
        bot.send_message(message.from_user.id, custom_daydata_request(valid_date))
        bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
        bot.set_state(message.from_user.id, UserDialogState.start_dialog)





@bot.message_handler(content_types=['text'],
                     func=lambda msg: msg.text == "Назад"  # Если ввели назад или нажали на кнопку
                     )
def handle_back_button(message: Message):
    bot.send_message(message.from_user.id, 'Возвращаю в начало диалога', reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog)  # Присваиваем состояние начала диалога



