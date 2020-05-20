from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import logg
import settings
import threading
import time
from ethadress import get_eth_address
from aave.code import do
from workers.montor_health import do as health
import database

import traceback
def error(update, context, error):
    """Log Errors caused by Updates."""
    logg.ERROR.warning('Update "%s" caused error "%s", error: %s', update, context, error)
    logg.ERROR.warning(traceback.format_exc())

def handle_inline_result(bot, update):
    s = database.Session()
    try:
        query = update.callback_query
        data = query.data
        if data.startswith("health"):
            factor = float(data.split(":")[1])
            database.HealthNotification.upsert(
                s,
                update.effective_user.id,
                get_eth_address(update.effective_user.id),
                factor
            )
            query.edit_message_text(
                text="Selected option, factor: %s" % factor)
        else:
            query.edit_message_text("Clicked deposit, a transaction link should follow if you run the right client")
        query.answer()
        s.commit()
    finally:
        s.close()

def handle_update_message(bot, update):
    if "/risk" in update.message.text:
        s = database.Session()
        d = database.HealthNotification.get(s, update.effective_user.id)
        health(d)
        s.close()
    elif "/start" in update.message.text:
        address = get_eth_address(update.effective_user.id)
        data = do(address, human=True)
        update.message.reply_text(
            "Hello your current health factor is <b>%s</b>, if your health factor gets "
            "below <b>1</b>, your are at risk to get liquidated, at what factor do you "
            "want to receive a notification?" % data["healthFactor"],
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text="1.1",
                    # function-gwei-args
                    callback_data="health:1.1"
                ),
                InlineKeyboardButton(
                    text="1.25",
                    # function-gwei-args
                    callback_data="health:1.25"
                ),
                InlineKeyboardButton(
                    text="1.5",
                    # function-gwei-args
                    callback_data="health:1.5"
                )
            ]]),
        )
    else:
        update.message.reply_text("try /start or /risk")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN)
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
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            updater.stop()
            break
        time.sleep(1)