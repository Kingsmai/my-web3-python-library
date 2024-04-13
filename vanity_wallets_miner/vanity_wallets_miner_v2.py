from eth_account import Account
import re
import csv
import time

# 要实现每 5 秒显示已经遍历的账户数量，我们可以在生成钱包的循环中加入计时和打印逻辑。以下是修改后的代码，加入了一个简单的计时机制来实现这个功能：

# 这段代码中，start_time 记录了每次检查周期的开始时间。在无限循环中，每当过去了 5 秒，就会打印当前已遍历的账户数量，并重置 start_time。这样，您就可以每 5 秒获得一次更新，了解已经遍历了多少个账户。

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
