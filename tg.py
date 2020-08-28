from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
import logg
import settings
import threading
import time
from aave.code import do

import traceback
def error(update, error):
    """Log Errors caused by Updates."""
    logg.ERROR.warning('Update "%s" caused error "%s"', update, error)
    logg.ERROR.warning(traceback.format_exc())

def handle_inline_result(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option:s".format(query.data))

def handle_update_message(update, context):
    address = update.effective_user.address
    data = do(address, human=True)
    update.message.reply_text("Hello your current health factor is %s" % data["healthFactor"])

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handle_update_message))
    dp.add_handler(MessageHandler(Filters.command, handle_update_message))
    dp.add_handler(CallbackQueryHandler(handle_inline_result))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()