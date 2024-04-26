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


def getZkSyncRPC() -> str:
    return random.choice(SEPOLIA_RPC_LIST)


w3 = Web3(Web3.HTTPProvider(getZkSyncRPC()))

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
# Transaction hash: 0x26b94e45de718c1d0a85d9fa2c7f7eb3bd19e4e9c90b575a28388d16dc4b92b4

# 等待交易被挖出
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Transaction receipt: {txn_receipt}")
# Transaction receipt: AttributeDict({'blockHash': HexBytes('0x8b881ab8e0000322091bb42d673d39e39d23bbfa769e422c7161fbc75b2c9a11'), 'blockNumber': 5778465, 'contractAddress': None, 'cumulativeGasUsed': 21000, 'effectiveGasPrice': 50000000000, 'from': '0xd88032e588EEe73bC3e682be4EcB9B740dfb014a', 'gasUsed': 21000, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0x369c54759Cb1AE18a897ED2c6230Cf2043b92eF9', 'transactionHash': HexBytes('0x26b94e45de718c1d0a85d9fa2c7f7eb3bd19e4e9c90b575a28388d16dc4b92b4'), 'transactionIndex': 0, 'type': 0})
