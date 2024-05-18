# Бот-помогатор
Telegram-бот для работы с API.
Бот-помогатор поможет мониторить цены авиаилетов на заданые направления.

## Содержание
- [Использование](#использование)
- [Разработка](#разработка)
- [FAQ](#FAQ)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)


## Использование
Он запускается с помощью клонирования репозитория и установки необходимых
библиотек (pip install -r requirements.txt) (пока в разработке)

Бот использует основные запросы:
```
Low - Самый дешевый билет Сочи -> Белград на завтра
```
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

```
High - Самый популярный билет Сочи -> Белград на завтра
```
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
```
Castom - Позволяет ввести дату и находит самый дешевый билет Сочи -> Белград на выбранный день
```
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

## Разработка
В целом бот функционирует, но официально сейчас находимся на 1 шаге из 6.

## FAQ 
Когда обнова? - Когда окнут API

### Зачем вы разработали этот проект?
Чтобы был.

## To do
- [x] Добавить крутое README
- [ ] Всё переписать
- [ ] ...

## Команда проекта
[Бердоносов Максим] — Back-End-junior Home developer

[Кошка Вася] - Chief Developer Assistant