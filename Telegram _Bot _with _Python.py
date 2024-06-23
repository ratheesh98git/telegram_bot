import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello, World!')

hello_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hello_handler)

def summary(update, context):
    response = requests.get('https://api.covid19api.com/summary')
    if response.status_code == 200:
        data = response.json()
        global_summary = data['Global']
        message = (
            f"COVID-19 Global Summary:\n"
            f"New Confirmed: {global_summary['NewConfirmed']}\n"
            f"Total Confirmed: {global_summary['TotalConfirmed']}\n"
            f"New Deaths: {global_summary['NewDeaths']}\n"
            f"Total Deaths: {global_summary['TotalDeaths']}\n"
            f"New Recovered: {global_summary['NewRecovered']}\n"
            f"Total Recovered: {global_summary['TotalRecovered']}\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error, something went wrong.")

summary_handler = CommandHandler('summary', summary)
dispatcher.add_handler(summary_handler)

def start(update, context):
    welcome_message = (
        "Welcome to the COVID-19 Tracker Bot!\n"
        "Use /hello to get a greeting.\n"
        "Use /summary to get the latest global COVID-19 summary.\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

dispatcher.add_error_handler(error)

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
