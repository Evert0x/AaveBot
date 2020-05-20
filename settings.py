from decouple import config
BOT_TOKEN=config("BOT_TOKEN")
MAPPER=config("MAPPER")
FLASK_HOST=config("FLASK_HOST", default="localhost")
FLASK_PORT=config("FLASK_PORT", cast=int, default=5000)