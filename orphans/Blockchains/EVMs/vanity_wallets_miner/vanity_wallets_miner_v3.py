from eth_account import Account
import re
import csv
import time

# 为了只输出地址尾号为5位连号及以上的地址和助记词，我们需要对之前的代码进行一些调整。下面是改进后的代码，这次我们将检查每个生成的钱包地址的尾号是否包含5位或更多连续相同的字符（0-9或a-f），如果满足条件，则将地址和对应的助记词写入文件：

# 在这个改进的代码中，我们使用Account.create_with_mnemonic()来同时生成钱包地址和助记词。当检测到一个地址的尾号满足连续相同字符的条件时，将该地址和对应的助记词一起写入文件。此外，我们在每5秒输出一次已经遍历的账户数量，以便跟踪进度。这个脚本会持续运行，直到你手动停止它（通过 CTRL + C）。生成的钱包地址和助记词将被存储在同目录下的wallets_with_consecutive_chars.csv文件中。

def has_consecutive_characters(string, min_length=5):
    # 使用正则表达式检查尾号是否存在连续字符
    return re.search(r'([0-9a-f])\1{' + str(min_length-1) + r',}$', string) is not None

def create_and_save_wallets():
    with open('wallets_with_consecutive_chars.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["钱包地址", "助记词"])

        count = 0  # 初始化计数器
        start_time = time.time()  # 记录开始时间

        while True:
            # 创建钱包和助记词
            Account.enable_unaudited_hdwallet_features()
            account, mnemonic = Account.create_with_mnemonic()
            address = account.address

            # 更新计数器
            count += 1

            # 检查是否已过5秒，并打印计数
            if time.time() - start_time >= 5:
                print(f"已遍历账户数量: {count}")
                start_time = time.time()  # 重置开始时间

            # 检查地址尾号中是否有五位以上连号
            if has_consecutive_characters(address.lower()):
                # 写入钱包地址和助记词
                csv_writer.writerow([address, mnemonic])

if __name__ == "__main__":
    print("---- 开始创建和存储钱包 ----")
    create_and_save_wallets()
