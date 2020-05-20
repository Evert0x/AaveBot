from telegram import Bot
import threading, time, database
from aave.code import do as monitor_status
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import settings, uuid
from web3 import Web3



def do(og_account=None):
    bot = Bot(settings.BOT_TOKEN)
    s = database.Session()
    for account in [og_account] if og_account else database.HealthNotification.get_all(s):
        data = monitor_status(account.address, human=True)
        healthFactor = data["healthFactor"]

        def get_good_factor(address, want_factor):
            data = monitor_status(address)
            maxBorrow = data["totalLiquidityETH"] * float(
                data["currentLiquidationThreshold"] / 100)
            currentBorrow = data["totalBorrowsETH"] + data["totalFeesETH"]
            # factor = maxBorrow / currentBorrow # current factor
            needMaxBorrow = want_factor * currentBorrow  # THe max borrow limit user needs
            toDeposit = needMaxBorrow - maxBorrow  # eth to deposit

            uuid_dai = str(uuid.uuid4()).replace("-", "")[:10]
            uuid_eth = str(uuid.uuid4()).replace("-", "")[:10]

            data = database.TxCall.insert(s, uuid_dai, account.userid, address=address, msg_id=0)
            data2 = database.TxCall.insert(s, uuid_eth, account.userid, address=address, msg_id=0)
            usd = float(Web3.fromWei(toDeposit, "ether")) * settings.ETH_PRICE
            return [data, data2], InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text="$%s in ETH" % round(usd, 2),
                    callback_data="%s-deposit-eth-%s-0" % (
                        uuid_dai, int(toDeposit))
                ),
                InlineKeyboardButton(
                    text="$%s in DAI" % round(usd, 2),
                    callback_data="%s-deposit-dai-%s-0" % (
                        uuid_eth, int(Web3.toWei(usd, "ether"))
                    )
                )
            ]])
        if healthFactor < account.factor:
            data, markup = get_good_factor(account.address,
                                           (account.factor + 0.05))

            msg = bot.send_message(
                chat_id=account.userid,
                parse_mode="html",
                text="You are at risk! Current factor: <b>%s</b>, please make a "
                     "deposit to get your health factor back to <b>%s</b>" % (healthFactor, account.factor),
                # Add some extra to the expected factor
                reply_markup=markup,
            )
            for x in data:
                x.msg_id = msg.message_id
            s.commit()
        elif og_account:
            bot.send_message(
                chat_id=account.userid,
                text="You are not at risk! Current factor: %s" % healthFactor
            )

    s.close()

def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(60)
        time.sleep(1)