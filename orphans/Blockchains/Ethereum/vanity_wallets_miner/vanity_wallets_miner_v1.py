from eth_account import Account
import re
import csv

# 使其持续生成钱包地址，并检查这些地址中是否存在五位以上连号。如果存在，就将地址和私钥写入文件中；如果不存在，就丢弃它们。这个过程将无限进行，直到你使用 CTRL + C 中断程序。

# 这段代码中的 has_consecutive_characters 函数使用了正则表达式来检查一个字符串是否包含五个或更多连续的相同字符。主函数 create_and_save_wallets 会无限循环地生成钱包，并调用 has_consecutive_characters 函数检查每个地址。如果地址符合条件，就将其写入 wallets_with_consecutive_chars.csv 文件中。

# 请注意，这个脚本会持续运行直到你手动停止（通过 CTRL + C）。生成的钱包信息将被存储在同目录下的 wallets_with_consecutive_chars.csv 文件中。

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
        
        while True:
            # 创建钱包
            account = Account.create()
            privateKey = account._key_obj
            address = account.address

            # 检查地址中是否有五位以上连号
            if has_consecutive_characters(address):
                # 写入钱包信息
                csv_writer.writerow([address, str(privateKey)])

if __name__ == "__main__":
    print("---- 开始创建和存储钱包 ----")
    
    # 无限生成钱包，直到程序被手动中断
    create_and_save_wallets()
