from loader import bot
from telebot.types import Message
from states.dialog_state import UserDialogState
from keyboards.reply.menu_keyboard import menu
from peewee import IntegrityError
from models import User


@bot.message_handler(commands=["start"], state="*") # Ловим команду
def handle_command(message: Message):
    bot.delete_state(message.from_user.id, message.chat.id)

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.reply_to(message, f"Добро пожаловать {first_name}!")
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {first_name}!")

    bot.send_message(message.from_user.id, '👋 Я твой бот-помошник!')  # welcome: Поздороваться
    bot.send_message(message.from_user.id, 'Могу помочь подобрать билеты на самолет по направлению'
                                           ' Сочи -> Белград. '
                                           '\nМожно выбрать готовые варианты на завтра или изменить дату',
                     reply_markup=menu())

    bot.set_state(message.from_user.id, UserDialogState.start_dialog) #TODO Думаю что вот этой строки не должно быть
                                                                    #   команды должны както по другому подключаться


