from telebot import types
from loader import bot
#from telebot.types import Message


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

#
# @bot.message_handler(commands=["start"])
# def bot_start(message: Message):
#     bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
