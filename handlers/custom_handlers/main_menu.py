import datetime
import time
import telebot
from telebot import types
from loader import bot
from telebot import types
import requests
import json
import os
#from . import main_menu
from dotenv import load_dotenv, find_dotenv
from loader import bot
from states.dialog_state import UserDialogState
from telebot.types import Message
from keyboards.reply.menu_keyboard import menu
from keyboards.reply.menu_keyboard import get_ticket
from keyboards.reply.menu_keyboard import cancel
from utils.misc.get_low_request import low_request
from utils.misc.get_high_request import high_request
from utils.misc.get_custom_daydata import custom_daydata_request



api_token = os.getenv("RAPID_API_KEY")
today = datetime.date.today()
print('main_menu Ready')
tomorrow = today + datetime.timedelta(days=1)
root_link = 'https://www.aviasales.ru'


def construct_answer(data):

    departure_at = data['data'][0]['departure_at']
    price = data['data'][0]['price']
    end_link = root_link + data['data'][0]['link']
    result = 'Нашел рейс Сочи -> Белград:\n' \
             'Дата отправления:{}\n' \
             'Цена:{} руб.\n' \
             'Ссылка: {}'.format(departure_at, price, end_link)
    return result


@bot.message_handler(commands=["start_dialog"]) # Ловим команду
def handle_command(message: Message):
    bot.send_message(message.from_user.id, '👋 Привет! Я твой бот-помошник!')  # welcome: Поздороваться
    bot.send_message(message.from_user.id, 'Могу помочь подобрать билеты на самолет по направлению'
                                           ' Сочи -> Белград. '
                                           '\nМожно выбрать готовые варианты на завтра или изменить дату',
                     reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog) # Присваиваем состояние
    # Отправляет в хендлер start_dialog и ждет сообщение

    #Останавливается здесь и ждет сообщение
@bot.message_handler(state=UserDialogState.start_dialog) # Ловим состояние
def handle_start_dialog(message: Message):
    #bot.send_message(message.from_user.id, 'Low or High??', reply_markup=menu())  # menu: Low, High, Назад
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
        if message.text == 'Отмена':  # TODO не понимаю почему эта кнопка не работает. Не хочет возвращаться в главное меню
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




'''

@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ближайший самолет Сочи -> Белград на завтра')
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)

    elif message.text == 'Ближайший самолет Сочи -> Белград на завтра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Low')
        btn2 = types.KeyboardButton('High')
        btn3 = types.KeyboardButton('Custom')
        btn4 = types.KeyboardButton('History')
        #btn5 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, '❓ Какой запрос нужен?', reply_markup=markup)

    elif message.text == 'Low':
        bot.register_next_step_handler(message, get_low_request)

    elif message.text == 'High':
        bot.register_next_step_handler(message, get_high_request)

    elif message.text == 'Custom':
        bot.send_message(message.from_user.id, 'Выдает кастомный ответ', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Хочешь поменять даты?', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Введите дату в формате yyyy-mm-dd    (main_menu)', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_castom_daydata)

    elif message.text == 'History':
        bot.send_message(message.from_user.id, 'Показывает историю запросов', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Пока не работает', parse_mode='Markdown')

    else:
        bot.send_message(message.from_user.id, 'Такой команды я не знаю', parse_mode='Markdown')
    #elif user_message == 'Назад':
        #bot.send_message(message.from_user.id, 'Возврат в главное меню', parse_mode='Markdown')

'''