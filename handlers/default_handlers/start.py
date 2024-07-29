from loader import bot
from telebot.types import Message
from states.dialog_state import UserDialogState
from keyboards.reply.menu_keyboard import menu
from handlers.custom_handlers import main_menu


@bot.message_handler(commands=["start"]) # Ловим команду
def handle_command(message: Message):
    bot.send_message(message.from_user.id, '👋 Привет! Я твой бот-помошник!')  # welcome: Поздороваться
    bot.send_message(message.from_user.id, 'Могу помочь подобрать билеты на самолет по направлению'
                                           ' Сочи -> Белград. '
                                           '\nМожно выбрать готовые варианты на завтра или изменить дату',
                     reply_markup=menu())
    bot.set_state(message.from_user.id, UserDialogState.start_dialog) #TODO Думаю что вот этой строки не должно быть
                                                                    #   команды должны както по другому подключаться

