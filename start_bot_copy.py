import datetime
import time
import telebot
from telebot import types
import requests
import json

# документация к API яндекс https://yandex.ru/dev/rasp/doc/ru/reference/schedule-point-point

bot = telebot.TeleBot('7076862024:AAFP0rijMMQJFeh9waQ_rDVFL03tKZGA67k')
#api_key = '3fcba97e-6f2f-4bfc-8ea1-15e33e222275'
api_token = '8d9dc41f692f04216d5adb57aafb5f2b'
api_partner_key = '545748'
# документация к API авиасейлс https://support.travelpayouts.com/hc/ru/articles/203956163-API-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-Aviasales-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D0%BE%D0%B2

today = datetime.date.today()
print(today)
tomorrow = today + datetime.timedelta(days=1)
print(tomorrow)
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


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '👋 Поздороваться' or message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ближайший самолет Сочи -> Белград на завтра')
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)

    elif message.text == 'Другое' or message.text == 'Ближайший самолет Сочи -> Белград на завтра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Low')
        btn2 = types.KeyboardButton('High')
        btn3 = types.KeyboardButton('Custom')
        btn4 = types.KeyboardButton('History')
        btn5 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, '❓ Какой запрос нужен?', reply_markup=markup)

    elif message.text == 'Low':
        bot.send_message(message.from_user.id, 'Самый дешевый билет Сочи -> Белград', parse_mode='Markdown')
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
                              'token={token}'.format(departure_at=tomorrow, token=api_token))

        data = json.loads(my_req.text)
        print('data ok')
        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Назад')
        btn2 = types.KeyboardButton('Другое')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, construct_answer(data), reply_markup=markup)
    
    elif message.text == 'High':
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
        btn2 = types.KeyboardButton('Другое')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, construct_answer(data), reply_markup=markup)

    elif message.text == 'Custom':
        bot.send_message(message.from_user.id, 'Выдает кастомный ответ', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Хочешь поменять даты?', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Введите дату в формате yyyy-mm-dd', parse_mode='Markdown')
        bot.register_next_step_handler(message, get_castom_daydata)


    elif message.text == 'History':
        bot.send_message(message.from_user.id, 'Показывает историю запросов', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Пока не работает', parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def get_castom_daydata(message):
    try:
        struct = time.strptime(message.text, '%Y-%m-%d')
        valid_date = time.strftime('%Y-%m-%d', struct)
        bot.send_message(message.from_user.id, 'Сейчас посмотрим', parse_mode='Markdown')
    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Назад')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Неверная дата, попробуй еще раз', reply_markup=markup)
        if message.text == 'Назад':
            bot.register_next_step_handler(message, get_text_messages)
        else:
            bot.register_next_step_handler(message, get_castom_daydata)
    else:
        bot.send_message(message.from_user.id, 'Самый дешевый билет Сочи -> Белград', parse_mode='Markdown')
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Назад')
        btn2 = types.KeyboardButton('Другое')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, construct_answer(data), reply_markup=markup)


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
#test
#bot.infinity_polling(skip_pending=True)