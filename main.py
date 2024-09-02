from telebot.custom_filters import StateFilter
import handlers  # noqa
from loader import bot
from utils.set_bot_commands import set_default_commands
from database.models import create_models

if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))  # Добавление поддержки состояний
    set_default_commands(bot)   # Добавление дефолтных команд
    bot.polling(none_stop=True, interval=0)







