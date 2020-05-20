from tg import main
import threading,settings
import sys
from server import app as flaskapp
from workers.montor_health import run
threads = []

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    for thread in threads:
        thread.do_run = False
        thread.join()
    sys.exit(0)

def interrupt():
    signal_handler(None, None)

def create_app():
    global threads
    t1 = threading.Thread(name="tgbot", target=main)
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(name="health", target=run)
    t2.start()
    threads.append(t2)
    return flaskapp

app = create_app()

if __name__ == '__main__':
    app.run(settings.FLASK_HOST, settings.FLASK_PORT)