import datetime
import time
import telebot
from telebot import types
from loader import bot
from telebot import types
import requests
import json
import os
from . import get_high_request
from . import get_low_request
from . import get_castom_daydata
#from . import main_menu
from dotenv import load_dotenv, find_dotenv


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