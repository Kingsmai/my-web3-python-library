from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_account.datastructures import SignedTransaction
from web3 import Web3
import random
from private import ORIGIN_PRIVATE_KEY, DEST_ADDRESS


origin_account: LocalAccount = Account.from_key(ORIGIN_PRIVATE_KEY)

SEPOLIA_RPC_LIST = [
    "https://1rpc.io/sepolia",
    "https://rpc-sepolia.rockx.com",
    "https://eth-sepolia-public.unifra.io",
    "https://eth-sepolia.public.blastapi.io",
    "https://ethereum-sepolia-rpc.publicnode.com",
    "https://ethereum-sepolia.rpc.subquery.network/public",
    "https://endpoints.omniatech.io/v1/eth/sepolia/public",
    "https://ethereum-sepolia.blockpi.network/v1/rpc/public",
]


def getSepoliaRPC() -> str:
    return random.choice(SEPOLIA_RPC_LIST)


w3 = Web3(Web3.HTTPProvider(getSepoliaRPC()))

# 检查连接是否成功
if w3.is_connected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")

balance_wei = w3.eth.get_balance(origin_account.address)
balance = w3.from_wei(balance_wei, "ether")

print(f"{origin_account.address} got {balance} ETH on zkSync Mainnet")

# 设置交易参数
transfer_amt = 2
transfer_amt_wei = w3.to_wei(transfer_amt, "ether")
chain_id = w3.eth.chain_id  # 获取当前链 ID

# 构造交易
transaction = {
    'to': DEST_ADDRESS,
    'value': transfer_amt_wei,
    'gas': 2000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(origin_account.address),
    'chainId': chain_id  # 添加 chainId 参数以支持 EIP-155
}

# 签名交易
signed_txn: SignedTransaction = w3.eth.account.sign_transaction(transaction, origin_account.key)

# 发送交易
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Transaction hash: {txn_hash.hex()}")


# 等待交易被挖出
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")
