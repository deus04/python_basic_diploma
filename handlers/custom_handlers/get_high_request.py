import datetime
import time
import telebot
from telebot import types
from loader import bot
from telebot import types
import requests
import json
import os
from . import get_castom_daydata
from dotenv import load_dotenv, find_dotenv
from . import main_menu


api_token = os.getenv("RAPID_API_KEY")
today = datetime.date.today()
print('high_request Ready')
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
def get_high_request(message):
    bot.send_message(message.from_user.id, 'Выдает максимальное значение', parse_mode='Markdown')
    bot.send_message(message.from_user.id, 'Самый популярный билет Сочи -> Белград', parse_mode='Markdown')
    my_req = requests.get('https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                          'origin=AER&'
                          'destination=BEG&'
                          'departure_at={departure_at}&'
                          'unique=true&'
                          'sorting=route&'
                          'direct=false&'
                          'currency=rub&'
                          'limit=10&'
                          'page=1&'
                          'one_way=true&'
                          'token={token}'.format(departure_at=tomorrow, token=api_token))

    data = json.loads(my_req.text)
    print('data ok')
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Назад')
    markup.add(btn1)
    bot.send_message(message.from_user.id, construct_answer(data), reply_markup=markup)
    if message.text == 'Назад':
        bot.register_next_step_handler(message, main_menu)
