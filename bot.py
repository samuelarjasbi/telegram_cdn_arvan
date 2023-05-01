import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import signal
import api
import jdatetime

# Replace YOUR_BOT_TOKEN with the token provided by the BotFather
bot = telegram.Bot(token='6140268578:AAG_mK1KajGdG_fHHKTIiqBj-aPQuO4uD8s')

# Define the command handler for the /start command
approved_chat_ids = [869388106,907246713]

def start(update, context):
    # Check the chat_id of the incoming message
    chat_id = update.message.chat_id
    if chat_id in approved_chat_ids:
        # Define the keyboard layout
        keyboard = [[InlineKeyboardButton("Server", callback_data='server')],[InlineKeyboardButton("All", callback_data='all')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the message with the keyboard layout
        update.message.reply_text('Welcome to ArvanCDNcloud monitoring', reply_markup=reply_markup)
    else:
        update.message.reply_text('Sorry, you are not authorized to use this bot.')

# Define the callback handler for the buttons
def button(update, context):
    query = update.callback_query
    if query.data == 'server':
        servers = api.get_servers()
        buttons = [[InlineKeyboardButton(server, callback_data=f'server_{server}')] for server in servers]
        reply_markup = InlineKeyboardMarkup(buttons)
        query.edit_message_text(text='Please choose a server:', reply_markup=reply_markup)
    elif query.data.startswith('server_'):
        server_name = query.data.replace('server_', '')
        now = jdatetime.datetime.now()
        data = api.point_data(server_name)
        # Do something with the selected server...
        query.edit_message_text(text=f"{data}\n📅<b>time:</b> {now.strftime('%Y/%m/%d %H:%M:%S')}",parse_mode=telegram.ParseMode.HTML)
    elif query.data == 'all':
        servers = api.get_servers()
        total_info = []
        now = jdatetime.datetime.now()
        with ThreadPoolExecutor() as executor:
            future_data = {executor.submit(api.point_data, server): server for server in servers}
            for future in concurrent.futures.as_completed(future_data):
                server = future_data[future]
                try:
                    data = future.result()
                    total_info.append(data)
                except Exception as exc:
                    print('%r generated an exception: %s' % (server, exc))
        query.edit_message_text(text=f'\n ----------------------------- \n'.join(total_info)+f"📅<b>time:</b> {now.strftime('%Y/%m/%d %H:%M:%S')}",parse_mode=telegram.ParseMode.HTML)
        
        




# Define the signal handler to stop the bot
def signal_handler(signal, frame):
    print('Stopping bot...')
    updater.stop()
    updater.is_idle = False


# Define the main function to start the bot
def main():
    # Create the updater and dispatcher
    global updater
    updater = Updater(token='6140268578:AAG_mK1KajGdG_fHHKTIiqBj-aPQuO4uD8s', use_context=True)
    dispatcher = updater.dispatcher

    # Define the command handler for the /start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Define the callback query handler for the buttons
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    # Start the bot
    updater.start_polling()

    # Register the signal handler to stop the bot
    signal.signal(signal.SIGINT, signal_handler)

    # Wait for the bot to stop
    updater.idle()


if __name__ == '__main__':
    main()
