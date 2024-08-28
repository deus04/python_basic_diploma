
from config_data import config
from telebot import StateMemoryStorage, TeleBot


storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)


