from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
import logg
import settings
import threading
import time
import aave.code as aave

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
    if update.message.text == "/start":
        update.message.reply_text("Hi, this is the unofficial Aave bot. Manage your Aave positions and receive interesting update.")
        if address:
            update.message.reply_text("Your current address is <b>%s</b>, do you want to get an overview of your positions? press /overview" % address, parse_mode="HTML")
        else:
            update.message.reply_text("You did not link your Ethereum address to your telegram account yet,"
            "please download the Totality fork or get in contact with @custodialbot")
        return

    if not address:
        update.message.reply_text("You did not link your Ethereum address to your telegram account yet,"
            "please download the Totality fork or get in contact with @custodialbot")
        return

    if update.message.text == "/overview":
        user_account = aave.get_user_account_data(address, human=True)
        balance = aave.get_user_balance(address, human=True)
        msg = "<b>Coin</b>\taToken/Total\n"
        for ticker, balances in balance.items():
            if balances["balance"] == 0 and balances["aBalance"] == 0:
                continue
            t = "<b>%s</b>\t<code>%s/%s</code> %s%% APY\n" % (ticker, balances["aBalance"],
                round(balances["aBalance"] + balances["balance"], 2),
                balances["APY"])
            msg += t
        update.message.reply_text("Healthfactor: <b>%s</b>\n\n%s" % (user_account["healthFactor"], msg), parse_mode="HTML")

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
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()