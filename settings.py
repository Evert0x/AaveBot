import os, json
from decouple import config
os.environ["TOTALITY_ENDPOINT"] = config("TOTALITY_ENDPOINT")

from web3 import Web3, HTTPProvider, WebsocketProvider
BOT_TOKEN=config("BOT_TOKEN")

ENDPOINT = Web3(HTTPProvider(config('PROVIDER')))
ENDPOINT_WS = Web3(WebsocketProvider(config('PROVIDER_WS')))

LPAddressProvider=config("LPAddressProvider")
LPCore=config("LPCore")
with open(os.path.join("aave", "abi", "LPAddressProvider.json")) as json_data:
    LPAddressProvider_ABI = json.load(json_data)
CONTRACT_LPAddressProvider = ENDPOINT.eth.contract(address=LPAddressProvider, abi=LPAddressProvider_ABI)

LP = CONTRACT_LPAddressProvider.functions.getLendingPool().call()
with open(os.path.join("aave", "abi", "LP.json")) as json_data:
    LP_ABI = json.load(json_data)
CONTRACT_LP = ENDPOINT.eth.contract(address=LP, abi=LP_ABI)
CONTRACT_LP_WS = ENDPOINT_WS.eth.contract(address=LP, abi=LP_ABI)
