import datetime
from loader import bot
from telebot import types
import requests
import json
import os



api_token = os.getenv("RAPID_API_KEY")
today = datetime.date.today()
print('low_request Ready')
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


def low_request():
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
    print(construct_answer(data))
    return construct_answer(data)
