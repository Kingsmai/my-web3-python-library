# 增加地址开头为 0x 连号的检测逻辑： 我们需要增加一个检查函数，来确定地址是否以 '0x' 开头并且之后的字符是否连续。

# 减少锁的使用： 尽量减少锁的使用，以避免线程间的竞争。例如，我们可以在本地对 count 进行计算，并定期更新共享变量，而不是每次生成地址后立即更新。

# 改进文件写入方式： 使用批量写入而不是每发现一个符合条件的地址就写入一次，这样可以减少文件操作的次数。

# 正则表达式编译： 编译正则表达式以提高匹配效率。

# 606410100

from eth_account import Account
import re
from multiprocessing import Process, Queue, Value
import time
import os

num_cores = os.cpu_count() or 4
num_workers = max(1, num_cores - 1)

# 预编译正则表达式
consecutive_pattern = re.compile(r'([0-9a-f])\1{4,}$')
start_with_0x_pattern = re.compile(r'^0x([0-9a-f])\1{4,}')

def has_consecutive_characters(string):
    return consecutive_pattern.search(string) is not None or start_with_0x_pattern.search(string) is not None

def wallet_generator(queue, count):
    local_count = 0
    Account.enable_unaudited_hdwallet_features()
    while True:
        account = Account.create()
        address = account.address.lower()  # 统一转为小写处理
        privateKey = account.key.hex()

        local_count += 1
        if local_count % 100 == 0:  # 每生成100个地址更新一次共享计数
            with count.get_lock():
                count.value += local_count
            local_count = 0

        if has_consecutive_characters(address):
            queue.put((address, privateKey))

def save_wallets(queue):
    while True:
        wallets = []
        while not queue.empty():
            wallets.append(queue.get())
        if wallets:
            with open('wallets_with_consecutive_chars.csv', 'a') as csv_file:
                for wallet in wallets:
                    csv_file.write(f"{wallet[0]},{wallet[1]}\n")

def monitor(count):
    while True:
        time.sleep(5)
        with count.get_lock():
            print(f"已遍历账户数量: {count.value}")

if __name__ == "__main__":
    queue = Queue()
    count = Value('i', 0)

    processes = [Process(target=wallet_generator, args=(queue, count)) for _ in range(num_workers)]
    saver = Process(target=save_wallets, args=(queue,))
    monitor_proc = Process(target=monitor, args=(count,))

    for p in processes:
        p.start()
    saver.start()
    monitor_proc.start()

    for p in processes:
        p.join()
    saver.join()
    monitor_proc.terminate()

    print("---- 完成 ----")
