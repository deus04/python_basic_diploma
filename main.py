from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()

api_key = '8d9dc41f692f04216d5adb57aafb5f2b'

