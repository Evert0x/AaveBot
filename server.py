from telegram import Bot
from flask import Flask
import database, settings
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/txhash/<code>/<tx>')
def hello_worldo(code, tx):
    s = database.Session()
    data = database.TxCall.get(s, code)
    b = Bot(settings.BOT_TOKEN)
    b.send_message(
        chat_id=data.userid,
        reply_to_message_id=data.msg_id,
        text="Transaction published successfully <a href=\"%s/tx/%s\">link</a>, please press /risk" % (
            "https://ropsten.etherscan.io", tx
        ),
        parse_mode="html",
        disable_web_page_preview=True

    )
    s.close()
    return 'Hello, World!'

@app.route("/txerror/<code>/<error>")
def err(code, error):
    s = database.Session()
    data = database.TxCall.get(s, code)
    b = Bot(settings.BOT_TOKEN)
    b.send_message(
        chat_id=data.userid,
        reply_to_message_id=data.msg_id,
        text="This failed with error %s" % error
    )
    s.close()
    return 'Hello, World!'