from eth_account import Account

if __name__ == '__main__':
    with open('wallet.csv', 'a') as wallet_file, open('address_only.csv', 'w', newline='') as address_file:
        # 为 address_only.csv 文件写入标题

        for i in range(1000):
            Account.enable_unaudited_hdwallet_features()
            account, mnemonic = Account.create_with_mnemonic()
            line = f'{account.address},{account.key.hex()},{mnemonic}\n'
            wallet_file.write(line)

            # 将地址单独写入 address_only.csv
            address_file.write(f'{account.address}\n')
