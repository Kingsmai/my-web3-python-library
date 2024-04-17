import csv
import random
from web3 import Web3

BINANCE_SMART_CHAIN_RPCS = [
    'https://bsc-pokt.nodies.app',
    'https://bsc.blockpi.network/v1/rpc/public',
    'https://bsc-dataseed1.bnbchain.org',
    'https://bsc-dataseed1.ninicoin.io'
    'https://bsc-dataseed1.defibit.io',
    'https://bsc-dataseed2.defibit.io',
    'https://bsc-dataseed3.defibit.io',
    'https://bsc-dataseed4.defibit.io',
    'https://public.stackup.sh/api/v1/node/bsc-mainnet',
    'https://rpc-bsc.48.club',
    'https://bsc-dataseed.bnbchain.org',
]

wallet_lists: list = []

with open("input/bsc.wallets.csv", 'r') as wallet_file:
    reader = csv.reader(wallet_file)
    for line in reader:
        wallet_lists.append(line[0])

for address in wallet_lists:
    w3: Web3 = Web3()
    while not w3.is_connected():
        rpc = random.choice(BINANCE_SMART_CHAIN_RPCS)
        print("Connecting RPC:", rpc)
        w3 = Web3(Web3.HTTPProvider(rpc))
    account_balance = w3.eth.get_balance(address)
    bsc_balance = w3.from_wei(account_balance, "ether")
    with open("output/bsc.wallets_balance.csv", "a") as output:
        writer = csv.writer(output)
        writer.writerow([address, bsc_balance])