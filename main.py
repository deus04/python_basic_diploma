from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.polling(none_stop=True, interval=0)
    #bot.infinity_polling()



