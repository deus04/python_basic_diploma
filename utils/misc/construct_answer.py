import datetime
import os


api_token = os.getenv("RAPID_API_KEY")
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
root_link = 'https://www.aviasales.ru'


def construct_answer(data):
    departure_at = data['data'][0]['departure_at']
    price = data['data'][0]['price']
    end_link = root_link + data['data'][0]['link']
# запись в историю
    result = 'Нашел рейс Сочи -> Белград:\n' \
             'Дата отправления:{}\n' \
             'Цена:{} руб.\n' \
             'Ссылка: {}'.format(departure_at, price, end_link)
    return result