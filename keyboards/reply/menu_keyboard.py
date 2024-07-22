from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def menu():
    keyboard = ReplyKeyboardMarkup(True, True)
    button_1 = KeyboardButton('Самый дешевый - Low')
    button_2 = KeyboardButton('Самый популярный - High')
    button_3 = KeyboardButton('Изменить дату')
    keyboard.add(button_1, button_2, button_3)
    return keyboard


def welcome():
    keyboard = ReplyKeyboardMarkup(True, True)
    button_1 = KeyboardButton('👋 Поздороваться')
    keyboard.add(button_1)
    return keyboard


def get_ticket():
    keyboard = ReplyKeyboardMarkup(True, True)
    button_1 = KeyboardButton('Получить')
    keyboard.add(button_1)
    return keyboard


def cancel():
    keyboard = ReplyKeyboardMarkup(True, True)
    button_1 = KeyboardButton('Отмена')
    keyboard.add(button_1)
    return keyboard

