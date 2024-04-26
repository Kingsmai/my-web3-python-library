# 增加地址开头为 0x 连号的检测逻辑： 我们需要增加一个检查函数，来确定地址是否以 '0x' 开头并且之后的字符是否连续。

# 减少锁的使用： 尽量减少锁的使用，以避免线程间的竞争。例如，我们可以在本地对 count 进行计算，并定期更新共享变量，而不是每次生成地址后立即更新。

# 改进文件写入方式： 使用批量写入而不是每发现一个符合条件的地址就写入一次，这样可以减少文件操作的次数。

# 正则表达式编译： 编译正则表达式以提高匹配效率。

# 导入相关模块
from eth_account import Account  # 用于生成 Ethereum 钱包
import re  # 用于使用正则表达式
from multiprocessing import Process, Queue, Value  # 用于多进程通信和数据共享
import time  # 用于时间控制
import os  # 用于操作系统相关操作

# 获取 CPU 核心数，如果获取失败默认为 4
num_cores = os.cpu_count() or 4
# 计算工作进程数，至少为 1
num_workers = max(1, num_cores - 1)

# 预编译正则表达式，用于匹配地址中是否存在连续相同的字符
consecutive_pattern = re.compile(r'([0-9a-f])\1{4,}$')  # 匹配地址末尾连续相同字符
start_with_0x_pattern = re.compile(r'^0x([0-9a-f])\1{4,}')  # 匹配以 '0x' 开头并且有连续相同字符的地址

# 检查字符串中是否有连续的字符，返回布尔值
def has_consecutive_characters(string):
    return consecutive_pattern.search(string) is not None or start_with_0x_pattern.search(string) is not None

# 钱包生成函数，每个工作进程会调用
def wallet_generator(queue, count):
    local_count = 0  # 本地计数器，用于统计生成的地址数量
    Account.enable_unaudited_hdwallet_features()  # 启用未经审计的高级钱包功能
    while True:
        account = Account.create()  # 创建新的钱包账户
        address = account.address.lower()  # 获取账户地址并转换为小写
        privateKey = account.key.hex()  # 获取私钥并转换为十六进制字符串

        local_count += 1
        if local_count % 100 == 0:  # 每生成 100 个地址后更新共享计数器
            with count.get_lock():
                count.value += local_count
            local_count = 0

        if has_consecutive_characters(address):  # 检查地址是否有连续字符
            queue.put((address, privateKey))  # 如果有，则将地址和私钥放入队列

# 钱包保存函数，用于将队列中的地址和私钥写入文件
def save_wallets(queue):
    while True:
        wallets = []
        while not queue.empty():
            wallets.append(queue.get())
        if wallets:
            with open('wallets_with_consecutive_chars.csv', 'a') as csv_file:
                for wallet in wallets:
                    csv_file.write(f"{wallet[0]},{wallet[1]}\n")

# 监视函数，定期打印已遍历的账户数量
def monitor(count):
    while True:
        time.sleep(5)
        with count.get_lock():
            print(f"已遍历账户数量: {count.value}")

# 主函数，初始化进程并启动它们
if __name__ == "__main__":
    queue = Queue()  # 创建队列，用于进程间通信
    count = Value('i', 0)  # 创建共享变量，用于跟踪生成的地址总数

    processes = [Process(target=wallet_generator, args=(queue, count)) for _ in range(num_workers)]  # 创建钱包生成进程
    saver = Process(target=save_wallets, args=(queue,))  # 创建保存钱包进程
    monitor_proc = Process(target=monitor, args=(count,))  # 创建监视进程

    for p in processes:
        p.start()  # 启动所有钱包生成进程
    saver.start()  # 启动保存进程
    monitor_proc.start()  # 启动监视进程

    for p in processes:
        p.join()  # 等待所有钱包生成进程结束
    saver.join()  # 等待保存进程结束
    monitor_proc.terminate()  # 强制终止监视进程

    print("---- 完成 ----")  # 打印完成信息
