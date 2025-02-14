# Бот-помогатор
Telegram-бот для работы с API.
Бот-помогатор поможет мониторить цены авиаилетов на заданые направления.

## Содержание
- [Установка](#установка)
- [Возможности бота](#возможности-бота)
- [FAQ](#FAQ)
- [Разработка](#разработка)
- [Команда проекта](#команда-проекта)


## Установка

Копировать репозиторий с ботом

Установить зависимости
> pip install -r requirements.txt

Создать файл `.env` и добавить туда `BOT_TOKEN` `RAPID_API_KEY`

Запустить бота `python main.py`



## Возможности бота

В боте представлены основные кнопки для поиска:

- Самый дешевый - Low
- Самый популярный - High
- Изменить дату

Так же можно воспользоваться командами:

- /start
- /help
- /history (История запросов(не более 10))

Бот использует основные запросы:

#### **Low - Самый дешевый билет Сочи -> Белград на завтра** 

Пример запроса:
```
'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                              'origin=AER&'
                              'destination=BEG&'
                              'departure_at=*ЗавтрашняяДата*&'
                              'unique=true&'
                              'sorting=price&'
                              'direct=false&'
                              'currency=rub&'
                              'limit=10&'
                              'page=1&'
                              'one_way=true&'
                              'token={token}
```
Ответ сервера:
```
{
    "data": [
        {
            "flight_number": "5069",
            "link": "/search/AER2005BEG1?t=A417161956001716268200001270AERISTESBBEG_522aefed5226b46856936eac0e664830_35714&search_date=19052024&expected_price_uuid=a8173f03-88fd-4db3-a007-c2ae4148ad01&expected_price_source=share&expected_price_currency=rub&expected_price=35714",
            "origin_airport": "AER",
            "destination_airport": "BEG",
            "departure_at": "2024-05-20T09:00:00+03:00",
            "airline": "A4",
            "destination": "BEG",
            "origin": "AER",
            "price": 35714,
            "return_transfers": 0,
            "duration": 1270,
            "duration_to": 315,
            "duration_back": 0,
            "transfers": 2
        }
    ],
    "currency": "rub",
    "success": true
}
```


#### **High - Самый популярный билет Сочи -> Белград на завтра**

Пример запроса:
```
'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                              'origin=AER&'
                              'destination=BEG&'
                              'departure_at=*ЗавтрашняяДата*&'
                              'unique=true&'
                              'sorting=route&'
                              'direct=false&'
                              'currency=rub&'
                              'limit=10&'
                              'page=1&'
                              'one_way=true&'
                              'token={token}'
```
Ответ сервера:
```
{
    "data": [
        {
            "flight_number": "5069",
            "link": "/search/AER2005BEG1?t=A417161956001716268200001270AERISTESBBEG_522aefed5226b46856936eac0e664830_35714&search_date=19052024&expected_price_uuid=a8173f03-88fd-4db3-a007-c2ae4148ad01&expected_price_source=share&expected_price_currency=rub&expected_price=35714",
            "origin_airport": "AER",
            "destination_airport": "BEG",
            "departure_at": "2024-05-20T09:00:00+03:00",
            "airline": "A4",
            "destination": "BEG",
            "origin": "AER",
            "price": 35714,
            "return_transfers": 0,
            "duration": 1270,
            "duration_to": 315,
            "duration_back": 0,
            "transfers": 2
        }
    ],
    "currency": "rub",
    "success": true
}
```

#### **Custom - Позволяет ввести дату и находит самый дешевый билет Сочи -> Белград на выбранный день**

Пример запроса:
```
'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?'
                              'origin=AER&'
                              'destination=BEG&'
                              'departure_at=*ЗавтрашняяДата*&'
                              'unique=true&'
                              'sorting=price&'
                              'direct=false&'
                              'currency=rub&'
                              'limit=10&'
                              'page=1&'
                              'one_way=true&'
                              'token={token}'
```
Ответ сервера:
```
{
    "data": [
        {
            "flight_number": "5073",
            "link": "/search/AER2505BEG1?t=A417166582001716807900002555AERISTSAWESBBEG_f22b96b4008e4add6191294bf9d48bb0_24209&search_date=19052024&expected_price_uuid=5018e4b7-1e0c-4579-bd27-9e0c8e0e7301&expected_price_source=share&expected_price_currency=rub&expected_price=24209",
            "origin_airport": "AER",
            "destination_airport": "BEG",
            "departure_at": "2024-05-25T17:30:00+03:00",
            "airline": "A4",
            "destination": "BEG",
            "origin": "AER",
            "price": 24209,
            "return_transfers": 0,
            "duration": 2555,
            "duration_to": 315,
            "duration_back": 0,
            "transfers": 2
        }
    ],
    "currency": "rub",
    "success": true
}
```



## FAQ 
Полезные ссылки:

[Документация к API](https://support.travelpayouts.com/hc/ru/articles/203956163-API-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-Aviasales-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%B0%D1%80%D1%82%D0%BD%D1%91%D1%80%D0%BE%D0%B2)

[Мануал по боту](https://core.telegram.org/bots) 

[Про RapidAPI](https://docs.rapidapi.com/docs/faqs)


## Разработка
Разработка бота завершена

## To do
- [x] Добавить README
- [x] Выбрать подходящее API
- [x] Написать базового бота
- [x] Добавить в него кнопки "High","Low","Custom" согласно ТЗ проекта.
- [x] Разложить код правильно согласно архитектуре проекта.
- [x] Добавить рабочую кнопку "History".
- [x] Оптимизировать код, доработать алгоритм.


## Команда проекта
[Бердоносов Максим] — Back-End-junior Home developer

[Кошка Вася] - Chief Developer Assistant