from telegram import Bot
import threading, time, database
from aave.code import do as monitor_status
import settings

def do(og_account=None):
    bot = Bot(settings.BOT_TOKEN)
    s = database.Session()
    for account in [og_account] if og_account else database.HealthNotification.get_all(s):
        data = monitor_status(account.address, human=True)
        healthFactor = data["healthFactor"]
        if healthFactor < account.factor:
            bot.send_message(
                chat_id=account.userid,
                text="You are at risk! Current factor: %s" % healthFactor
            )
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