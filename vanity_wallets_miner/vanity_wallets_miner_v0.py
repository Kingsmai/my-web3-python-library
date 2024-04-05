from eth_account import Account
import re
import csv
import time

def has_consecutive_characters(string, min_length=5):
    # 使用正则表达式检查是否存在连续字符
    for char in set(string):
        if char * min_length in string:
            return True
    return False

def create_and_save_wallets():
    with open('wallets_with_consecutive_chars.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["钱包地址", "私钥"])
        
        count = 0  # 初始化计数器
        start_time = time.time()  # 记录开始时间

        while True:
            # 创建钱包
            account = Account.create()
            privateKey = account._key_obj
            address = account.address

            # 更新计数器
            count += 1

            # 检查是否已过5秒，并打印计数
            if time.time() - start_time >= 5:
                print(f"已遍历账户数量: {count}")
                start_time = time.time()  # 重置开始时间

            # 检查地址中是否有五位以上连号
            if has_consecutive_characters(address):
                # 写入钱包信息
                csv_writer.writerow([address, str(privateKey)])

if __name__ == "__main__":
    print("---- 开始创建和存储钱包 ----")
    create_and_save_wallets()
