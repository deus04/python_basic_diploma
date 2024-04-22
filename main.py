from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()

api_key = '3fcba97e-6f2f-4bfc-8ea1-15e33e222275'

