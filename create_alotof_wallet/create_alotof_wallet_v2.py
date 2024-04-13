from eth_account import Account
import csv

def create_and_save_eth_wallets(total_wallets=1000000, num_files=10):
    # 每个文件要存储的钱包数量
    wallets_per_file = total_wallets // num_files
    file_index = 1
    wallet_count = 0
    
    # 初始化 CSV 文件和写入器
    csv_file = open(f'wallets_{file_index}.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])

    for id in range(total_wallets):
        # 添加随机性
        account = Account.create('Random Seed' + str(id))
        # 私钥
        privateKey = account._key_obj
        # 公钥
        publicKey = privateKey.public_key
        # 钱包地址
        address = publicKey.to_checksum_address()

        # 写入钱包信息到 CSV
        csv_writer.writerow([id, address, privateKey, publicKey])

        wallet_count += 1
        # 判断是否需要更换新的文件进行写入
        if wallet_count >= wallets_per_file:
            csv_file.close()
            file_index += 1
            wallet_count = 0
            if file_index <= num_files:  # 防止创建额外的文件
                csv_file = open(f'wallets_{file_index}.csv', 'w', newline='')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])

    # 关闭最后一个文件
    csv_file.close()

if __name__ == "__main__":
    print("---- 开始创建钱包 ----")
    create_and_save_eth_wallets()
    print("---- 完成 ----")
