import datetime
import telebot
from telebot import types
import requests
import json

# документация к API https://yandex.ru/dev/rasp/doc/ru/reference/schedule-point-point

bot = telebot.TeleBot('7076862024:AAFP0rijMMQJFeh9waQ_rDVFL03tKZGA67k')
api_key = '3fcba97e-6f2f-4bfc-8ea1-15e33e222275'
today = datetime.date.today()
data_today = today + datetime.timedelta(days=1)

def get_nearest(data):

    title = data['segments'][0]['thread']['title']
    number = data['segments'][0]['thread']['number']
    departure = data['segments'][0]['departure']
    result = 'Ближайший поезд на {} номер {} {} \n' \
             'отправление в {}'.format(str(data_today), number, title, departure[11:16])

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
        btn1 = types.KeyboardButton('Ближайший поезд на завтра')
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup)

    elif message.text == 'Ближайший поезд на завтра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Краснодар -> Каневская')
        markup.add(btn1)
        bot.send_message(message.from_user.id, '❓ Пункт отправления', reply_markup=markup) #ответ бота

    elif message.text == 'Краснодар -> Каневская':
        my_req = requests.get('https://api.rasp.yandex.net/v3.0/search/?apikey={}&format=json&from=s9613602&to=s9613146&lang=ru_RU&page=1&date={}&limit=100'.format(api_key, data_today))

        data = json.loads(my_req.text)
        print('data ok')
        with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        btn1 = types.KeyboardButton('Назад')
        markup.add(btn1)
        bot.send_message(message.from_user.id, get_nearest(data), reply_markup=markup)


'''
        #btn2 = types.KeyboardButton('High')
        #btn3 = types.KeyboardButton('Custom')
        #btn4 = types.KeyboardButton('History')
        #markup.add(btn1, btn2, btn3, btn4)
        

    elif message.text == 'Low':
        bot.send_message(message.from_user.id, data, parse_mode='Markdown')
    
    elif message.text == 'High':
        bot.send_message(message.from_user.id, 'Выдает максимальное значение', parse_mode='Markdown')

    elif message.text == 'Custom':
        bot.send_message(message.from_user.id, 'Выдает кастомный ответ', parse_mode='Markdown')

    elif message.text == 'History':
        bot.send_message(message.from_user.id, 'Показывает историю запросов', parse_mode='Markdown')
'''

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
#test