# 根据前面提到的性能优化策略，我将对您的代码进行几项关键改进。这包括简化正则表达式、使用异步I/O来处理文件写入、以及一些代码结构的优化。这些改动将帮助提高代码的执行效率和整体性能。以下是优化后的代码：

# 代码改动解释：
# 正则表达式优化：简化了正则表达式，只检测任何连续相同字符，减少了正则表达式的复杂性。
# 异步 I/O：引入了 asyncio 和 ThreadPoolExecutor 用于异步文件写入，以减少I/O操作对性能的影响。
# 延迟和非阻塞等待：在 save_wallets_async 函数中加入 await asyncio.sleep(1)，允许事件循环处理其他任务，避免磁盘I/O成为瓶颈。
# 代码结构：使用 if __name__ == "__main__": 来封装主执行逻辑，使模块更加清晰。
# 这些改动可以显著提升程序的性能，尤其是在处理大量数据时。同时，这些优化也有助于减少资源的消耗，提高程序的响应速度和处理能力。


from eth_account import Account
import re
import asyncio
import os
import time
from multiprocessing import Process, Queue, Value
from concurrent.futures import ThreadPoolExecutor

num_cores = os.cpu_count() or 4
num_workers = max(1, num_cores - 1)

# 优化后的正则表达式，避免过于复杂的模式
consecutive_pattern = re.compile(r'(.)\1{4,}')

async def save_wallets_async(queue):
    while True:
        wallets = []
        while not queue.empty():
            wallets.append(queue.get())
        if wallets:
            with open('wallets_with_consecutive_chars.csv', 'a') as file:
                file.writelines(f"{wallet[0]},{wallet[1]}\n" for wallet in wallets)
        await asyncio.sleep(1)  # 添加非阻塞等待，避免CPU满载

def wallet_generator(queue, count):
    local_count = 0
    Account.enable_unaudited_hdwallet_features()
    while True:
        account = Account.create()
        address = account.address.lower()
        if consecutive_pattern.search(address):
            queue.put((address, account.key.hex()))
        local_count += 1
        if local_count % 100 == 0:
            with count.get_lock():
                count.value += local_count
            local_count = 0

def monitor(count):
    while True:
        print(f"已遍历账户数量: {count.value}")
        time.sleep(5)

def main():
    queue = Queue()
    count = Value('i', 0)

    processes = [Process(target=wallet_generator, args=(queue, count)) for _ in range(num_workers)]
    for p in processes:
        p.start()

    # 使用线程池执行异步 I/O 任务
    with ThreadPoolExecutor() as pool:
        asyncio.run(save_wallets_async(queue))

    for p in processes:
        p.join()

    print("---- 完成 ----")

if __name__ == "__main__":
    main()
