from eth_account import Account

if __name__ == '__main__':
    with open ('wallet.txt', 'a') as wallet_file:
        for i in range(10000):
            Account.enable_unaudited_hdwallet_features()
            # account = Account.create()
            account, mnemonic = Account.create_with_mnemonic()
            line = '%s,%s,%s' % (account.address, account.key.hex(), mnemonic)
            wallet_file.write(line + '\n')