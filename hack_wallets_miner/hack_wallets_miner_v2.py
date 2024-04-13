from eth_account import Account
import os
from multiprocessing import Process, Queue, Value
import time
import asyncio
import aiofiles

num_cores = os.cpu_count() or 4
num_workers = max(1, num_cores - 1)

def wallet_generator(queue, count):
    local_count = 0  # 本地计数器，用于统计生成的地址数量
    while True:
        account = Account.create()
        address = account.address.lower()
        privateKey = account.key.hex()
        queue.put((address, privateKey))
        local_count += 1
        if local_count % 10000 == 0:  # 每生成 100 个地址后更新共享计数器
            with count.get_lock():
                count.value += local_count
            local_count = 0

async def save_wallets(queue):
    file_index = 1
    wallets = []
    last_save_time = time.time()
    while True:
        # 不断从队列中获取新的钱包地址
        while not queue.empty():
            wallets.append(queue.get())

        # 检查是否达到保存阈值或超过了最大等待时间（例如，5分钟）
        current_time = time.time()
        if len(wallets) >= 100000 or (current_time - last_save_time > 300):
            if wallets:
                async with aiofiles.open(f'wallets_{file_index}.csv', 'w') as file:
                    await file.writelines(f"{wallet[0]},{wallet[1]}\n" for wallet in wallets)
                wallets.clear()
                file_index += 1
                last_save_time = current_time

        # 等待一段时间再次检查队列，以减少CPU使用
        await asyncio.sleep(1)


def monitor(count):
    while True:
        time.sleep(5)
        print(f"已遍历账户数量: {count.value}")

def start_async_process(target, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(target(*args))
    loop.close()

def main():
    queue = Queue()
    count = Value('i', 0)

    processes = [Process(target=wallet_generator, args=(queue, count)) for _ in range(num_workers)]
    saver = Process(target=start_async_process, args=(save_wallets, queue))
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
