# 去掉公钥版本
from eth_account import Account
import csv
from queue import Queue
from threading import Thread

# 设置全局变量
total_wallets = 1000000
num_files = 10
wallets_per_file = total_wallets // num_files
queue = Queue()

def wallet_generator(queue, total_wallets):
    for id in range(total_wallets):
        account = Account.create('Random Seed' + str(id))
        privateKey = account._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        queue.put([id, address, str(privateKey), str(publicKey)])

def wallet_saver(queue, file_index):
    csv_file = open(f'wallets_{file_index}.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["序号", "钱包地址", "私钥", "公钥"])
    
    while True:
        wallet = queue.get()
        if wallet is None:
            break  # 结束信号
        csv_writer.writerow(wallet)
        queue.task_done()
    
    csv_file.close()

if __name__ == "__main__":
    print("---- 开始创建钱包 ----")

    # 启动钱包生成线程
    producer = Thread(target=wallet_generator, args=(queue, total_wallets))
    producer.start()

    # 启动多个钱包保存线程
    consumers = []
    for i in range(num_files):
        consumer = Thread(target=wallet_saver, args=(queue, i + 1))
        consumer.start()
        consumers.append(consumer)

    # 等待钱包生成线程结束
    producer.join()

    # 发送结束信号给消费者线程
    for _ in range(num_files):
        queue.put(None)

    # 等待所有消费者线程结束
    for consumer in consumers:
        consumer.join()

    print("---- 完成 ----")
