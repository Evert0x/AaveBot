import os
import settings
from web3 import Web3
import datetime
import json

with open(os.path.join("aave", "atokens.json")) as f:
    atokens = json.load(f)

with open(os.path.join("aave", "abi", "AToken.json")) as json_data:
    aTokenAbi = json.load(json_data)

def get_user_balance(user, human=False):
    data = {}
    # if os.path.exists("user.json"):
    #     with open("temp.json", "r") as f:
    #         return json.load(f)
    for ticker, contracts in atokens.items():
        if not contracts.get("aave"):
            continue

        reserveData = settings.CONTRACT_LP.functions.getUserReserveData(contracts["regular"], user).call()
        print(reserveData)
        aBalance = reserveData[0]
        liquidityRate = reserveData[5]

        if ticker == "ETH":
            balance = settings.ENDPOINT.eth.getBalance(user)
        else:
            contract = settings.ENDPOINT.eth.contract(address=contracts["regular"], abi=aTokenAbi)
            balance = contract.functions.balanceOf(user).call()

        if human:
            aBalance = round(float(Web3.fromWei(aBalance, "ether")), 2)
            balance = round(float(Web3.fromWei(balance, "ether")), 2)
            liquidityRate = round(float(liquidityRate/10000000000000000000000000), 2)

        data[ticker] = {
            "balance": balance,
            "aBalance": aBalance,
            "APY": liquidityRate
        }
    # with open("user.json", "w+") as f:
    #     json.dump(data, f, indent=4)
    return data

def get_user_account_data(address, human=False):
    data = settings.CONTRACT_LP_WS.functions.getUserAccountData(address).call()
    rt = {
        "totalLiquidityETH": data[0],
        "totalCollateralETH": data[1],
        "totalBorrowsETH": data[2],
        "totalFeesETH": data[3],
        "availableBorrowsETH": data[4],
        "currentLiquidationThreshold": data[5],
        "ltv": data[6],
        "healthFactor": data[7],
    }
    if human:
        # Divide all numbers by 1 with 18 zeros
        for k, v in rt.items():
            rt[k] = round(float(Web3.fromWei(v, "ether")), 2)

    return rt
