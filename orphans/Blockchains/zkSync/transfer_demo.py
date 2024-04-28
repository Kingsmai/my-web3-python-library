from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
import random
from private import ORIGIN_PRIVATE_KEY, DEST_ADDRESS


origin_account: LocalAccount = Account.from_key(ORIGIN_PRIVATE_KEY)
dest_account: LocalAccount = Account.from_key()

ZKSYNC_RPC_LIST = [
    "https://zksync-era.blockpi.network/v1/rpc/public",
    "https://go.getblock.io/f76c09905def4618a34946bf71851542",
    "https://zksync.meowrpc.com",
    "https://zksync.drpc.org",
    "https://1rpc.io/zksync2-era",
    "https://endpoints.omniatech.io/v1/zksync-era/mainnet/public",
    "https://mainnet.era.zksync.io",
    ""
]


def getZkSyncRPC() -> str:
    return random.choice(ZKSYNC_RPC_LIST)


w3 = Web3(Web3.HTTPProvider(getZkSyncRPC()))

