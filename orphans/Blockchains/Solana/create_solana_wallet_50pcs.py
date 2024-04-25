import utils.mnemonic_helper as mnemonic
import utils.solana_helper as sol

import datetime

current_time = datetime.datetime.now()
current_time_str = current_time.strftime("%Y%m%d")

lines_addr_mnemo = ""

for i in range(10000):
    mnemo = mnemonic.get_12_seed()
    sol_public_key = sol.get_solana_keys_from_mnemonic(mnemo)
    lines_addr_mnemo += f'{sol_public_key},{mnemo}\n'

with open(f'{current_time_str}_sol_wallets.csv', 'a') as file:
    file.writelines(lines_addr_mnemo)