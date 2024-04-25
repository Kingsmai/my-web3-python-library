from eth_account import Account
import csv
from threading import Thread

# 设置全局变量
total_wallets = 1000000
num_files = 10
wallets_per_file = total_wallets // num_files

def create_and_save_wallets(file_index, num_wallets):
    csv_file = open(f'wallets_{file_index}.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["序号", "钱包地址", "私钥"])

    for _ in range(num_wallets):
        # 创建钱包
        account = Account.create()
        privateKey = account._key_obj
        address = account.address

        # 写入钱包信息
        csv_writer.writerow([_, address, str(privateKey)])

    csv_file.close()

if __name__ == "__main__":
    print("---- 开始创建和存储钱包 ----")

    threads = []
    for i in range(num_files):
        # 为每个文件创建一个线程
        thread = Thread(target=create_and_save_wallets, args=(i+1, wallets_per_file))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("---- 完成 ----")
