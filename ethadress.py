import settings
import requests

def get_eth_address(tg_id):
    r = requests.get("%s/get/%s" % (
        settings.MAPPER, tg_id
    )).json()
    if r["status"]:
        return r["address"]
    return None