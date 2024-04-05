import utils.mnemonic_helper as mnemonic
import utils.solana_helper as sol

import datetime

current_time = datetime.datetime.now()
current_time_str = current_time.strftime("%Y%m%d")

lines_addr_mnemo = ""
lines_addr = ""
lines_mnemo = ""

for i in range(10):
    mnemo = mnemonic.get_12_seed()
    parent_address_last_6 = sol.get_solana_keys_from_mnemonic(mnemo)[-6:]
    for j in range(10):
        sol_public_key = sol.get_solana_keys_from_mnemonic(mnemo, j)
        if j == 0:
            lines_addr_mnemo += f'{parent_address_last_6}.{j + 1},{sol_public_key},{mnemo}\n'
        else:
            lines_addr_mnemo += f'{parent_address_last_6}.{j + 1},{sol_public_key},\n'
        lines_addr += f'{parent_address_last_6}.{j + 1},{sol_public_key}\n'
    lines_mnemo += f'{mnemo}\n'

with open(f'{current_time_str}_sol_wallets.csv', 'w') as file:
    file.writelines(lines_addr_mnemo)

with open(f'{current_time_str}_sol_addrs.csv', 'w') as file:
    file.writelines(lines_addr)

with open(f'{current_time_str}_sol_mnemos.csv', 'w') as file:
    file.writelines(lines_mnemo)