import datetime
import time
import telebot
from telebot import types
from loader import bot
from telebot import types
from handlers.custom_handlers import main_menu
import requests
import json
import os
#from . import get_castom_daydata



api_token = os.getenv("RAPID_API_KEY")
today = datetime.date.today()
print('castom_daydata Ready')
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


def custom_daydata_request(valid_date):
    '''
    try:
        struct = time.strptime(message.text, '%Y-%m-%d')
        valid_date = time.strftime('%Y-%m-%d', struct)
        bot.send_message(message.from_user.id, 'Сейчас посмотрим', parse_mode='Markdown')
    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Назад')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Неверная дата, попробуй еще раз', reply_markup=markup)
        print(message.text)
        if message.text == 'Назад':  #
            print('1')
            bot.register_next_step_handler(message, main_menu)
        else:
            print('2')
            bot.register_next_step_handler(message, get_castom_daydata)
        print('after', message.text)
    else:
    '''
    my_req = requests.get('https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                          'origin=AER&'
                          'destination=BEG&'
                          'departure_at={departure_at}&'
                          'unique=true&'
                          'sorting=price&'
                          'direct=false&'
                          'currency=rub&'
                          'limit=10&'
                          'page=1&'
                          'one_way=true&'
                          'token={token}'.format(departure_at=valid_date, token=api_token))

    data = json.loads(my_req.text)
    print('data ok')
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(construct_answer(data))
    return construct_answer(data)


'''
@bot.message_handler(content_types=['text'])
def wrong_castom_daydata(message):
    bot.send_message(message.from_user.id, 'верхушка вронг кастом', parse_mode='Markdown')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('Попробовать снова')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'Неверная дата, попробуете еще раз?   (wrong_castom_daydata)', reply_markup=markup)
    if message.text == 'Назад':
        bot.register_next_step_handler(message, main_menu)
    elif message.text == 'Попробовать снова':
        bot.register_next_step_handler(message, get_castom_daydata)
'''
