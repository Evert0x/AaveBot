# AaveBot
Telegram chatbot for liquidation warnings of Aave positions

Start chatting with https://t.me/EasyAave_bot

## Flow
When users start chatting, their Ethereum address is retreived from the mapper. 
This will only work if users use the Telegram Totality client (https://github.com/Evert0x/Telegram).

The Aave lending pool is being queried to retreive the account data that belongs to the user. 
Users are able to set a preferred `healt_factor` (more info on health factor: https://docs.aave.com/developers/other-documentation/glossary)
If the health factor gets below the set threshold, the user will receive a notification with an immediate call to action to 
get the health factor back to the preferred threshold. (Only works with the Telegram Totality client)

![In chat buttons](https://i.imgur.com/n44f2eK.png)

## Run it yourself

**Fill in .env file**

BOT_TOKEN={bot_token}</br>
MAPPER={mapper}</br>
LPAddressProvider=0x1c8756FD2B28e9426CDBDcC7E3c4d64fa9A54728</br>
PROVIDER=https://ropsten.infura.io/v3/{infura_token}</br>
PROVIDER_WS=wss://ropsten.infura.io/ws/v3/{infura_token}</br>
FLASK_HOST=localhost</br>
FLASK_PORT=5000


- `python database.py`, create SQLite database
- `pip install -r requirements.txt`, install all dependencies (virtualenv recommended)
- `python app.py`, run the application
