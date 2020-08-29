from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineTotalityMarkup, InlineTotalityButton
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler, CommandHandler
from web3 import Web3
import logg
import settings
import threading
import time
import aave.code as aave

import traceback
AMOUNT = range(1)
def error(update, error):
    """Log Errors caused by Updates."""
    logg.ERROR.warning('Update "%s" caused error "%s"', update, error)
    logg.ERROR.warning(traceback.format_exc())

def deposit_amount(update, context):
    ticker = context.user_data.get("ticker")
    if not ticker:
        update.message.reply_text("please select a ticker")
        return
    if float(update.message.text) > ticker["m"]:
        update.message.reply_text("It exceeds your max amount of %s" % ticker["m"])
        return

    weiValue = 0
    if ticker["t"] == "ETH":
        weiValue = Web3.toWei(float(update.message.text), 'ether')

    keyboard = InlineTotalityMarkup(settings.CONTRACT_LP.functions.deposit(
            Web3.toChecksumAddress(aave.atokens[ticker["t"]]["regular"]),
            Web3.toWei(float(update.message.text), 'ether'),
            0
    ), Web3.toWei("2", "gwei"), 500000, weiValue=weiValue)

    update.message.reply_text('Deposit %s %s' % (update.message.text, ticker["t"]), reply_markup=keyboard)
    del context.user_data["ticker"]
    return ConversationHandler.END

def handle_inline_result(update, context):
    query = update.callback_query
    query.answer()
    if query.data.startswith("tg"):
        if context.totality["canceled"]:
            if context.totality["tx"]:
                return query.edit_message_text(text="You clicked cancel BUT got tx: %s" % context.totality["tx"])
            return query.edit_message_text(text="You clicked cancel")

        if not context.totality["tx"]:
            query.edit_message_text(text="<b>Please chose custodial bot</b>\n%s" % update.callback_query.message.text,
            reply_markup=update.callback_query.message.reply_markup,
            parse_mode="HTML")
        else:
            query.edit_message_text(text="You clicked do with tx: %s" % context.totality["tx"])
        return

    balance = aave.get_user_balance(update.effective_user.address, filter_ticker=query.data, human=True)[query.data]
    context.user_data["ticker"] = {"t": query.data, "m": balance["balance"]}
    query.edit_message_text(
        text="How much %s do you want to deposit? Your max is <b>%s</b>" % (query.data, balance["balance"]),
        parse_mode="HTML"
    )

def handle_overview(update, context):
    address = update.effective_user.address
    if not address:
        update.message.reply_text("You did not link your Ethereum address to your telegram account yet,"
            "please download the Totality fork or get in contact with @custodialbot")
        return

    user_account = aave.get_user_account_data(address, human=True)
    balance = aave.get_user_balance(address, human=True)

    canDeposit = []
    msg = "<b>Coin</b>\taToken/Total\n"
    for ticker, balances in balance.items():
        if balances["balance"] == 0 and balances["aBalance"] == 0:
            continue
        t = "<b>%s</b>\t<code>%s/%s</code> %s%% APY\n" % (ticker, balances["aBalance"],
            round(balances["aBalance"] + balances["balance"], 2),
            balances["APY"])
        msg += t

        if balances["balance"] > 0:
            canDeposit.append(ticker)

    update.message.reply_text("Healthfactor: <b>%s</b>\n\n%s" % (user_account["healthFactor"], msg), parse_mode="HTML")
    if len(canDeposit) > 0:
        keyboard = []
        for ticker in canDeposit:
            keyboard.append(InlineKeyboardButton(ticker, callback_data=ticker))
        reply_markup = InlineKeyboardMarkup([keyboard])
        update.message.reply_text("You are able to convert your tokens to Atokens to receive interest", reply_markup=reply_markup)
        return AMOUNT

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


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('overview', handle_overview)],
        states={
            AMOUNT: [MessageHandler(Filters.regex("^[0-9]+([,.][0-9]+)?$"), deposit_amount)],

        },
        fallbacks=[
            CommandHandler('overview', handle_overview),
            CommandHandler('start', handle_update_message)
        ]
    )
    dp.add_handler(conv_handler)
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