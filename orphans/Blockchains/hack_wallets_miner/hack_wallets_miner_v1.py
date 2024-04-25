from eth_account import Account
import os
from multiprocessing import Process, Queue, Value
import time

num_cores = os.cpu_count() or 4  # 获取 CPU 核心数，默认为 4
num_workers = max(1, num_cores - 1)  # 设置工作进程数，至少为 1

def wallet_generator(queue, count):
    local_count = 0  # 本地计数器，用于统计生成的地址数量
    while True:
        account = Account.create()  # 创建新的钱包账户
        address = account.address.lower()  # 获取账户地址并转换为小写
        privateKey = account.key.hex()  # 获取私钥并转换为十六进制字符串
        queue.put((address, privateKey))  # 将地址和私钥放入队列

        local_count += 1
        if local_count % 10000 == 0:  # 每生成 100 个地址后更新共享计数器
            with count.get_lock():
                count.value += local_count
            local_count = 0

def save_wallets(queue):
    file_index = 1
    wallets = []
    while True:
        while not queue.empty():
            wallets.append(queue.get())
            if len(wallets) >= 100000:  # 每 100,000 个地址保存到一个文件
                with open(f'wallets_{file_index}.csv', 'w') as file:
                    file.writelines(f"{wallet[0]},{wallet[1]}\n" for wallet in wallets)
                wallets = []  # 清空列表以用于下一批地址
                file_index += 1  # 文件索引递增

def monitor(count):
    while True:
        time.sleep(5)  # 每 5 秒输出一次当前生成的地址数量
        with count.get_lock():
            print(f"已遍历账户数量: {count.value}")

def main():
    queue = Queue()
    count = Value('i', 0)  # 使用共享变量来跟踪生成的地址总数

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

if __name__ == "__main__":
    main()
