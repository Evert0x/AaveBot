import settings
from web3 import Web3

def do(address, human=False):
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
