from settings import CONTRACT_LP, ENDPOINT
from web3 import Web3

dai = "0xf80A32A835F79D7787E8a8ee5721D0fEaFd78108"
address = "0x662dBcB0445a1E49CD76B2473EBF4951778cAE4C"
pk = "821b676806784e5dc33da2e29ec5ec09e094f35b5facb1163c725802e6fa3f63"

data = {
    'chainId': 3,
    'gas': Web3.toHex(5000000),
    'gasPrice': Web3.toWei('5', 'gwei'),
    'nonce': ENDPOINT.eth.getTransactionCount(address),
}

ctr = CONTRACT_LP.functions.borrow(
    "0xB36938c51c4f67e5E1112eb11916ed70A772bD75", # usdt
    Web3.toWei(0.50, "ether"),
    1,
    0
).buildTransaction(data)

signed_tx = ENDPOINT.eth.account.sign_transaction(ctr, pk)
ENDPOINT.eth.sendRawTransaction(signed_tx.rawTransaction)
print(Web3.toHex(signed_tx["hash"]))