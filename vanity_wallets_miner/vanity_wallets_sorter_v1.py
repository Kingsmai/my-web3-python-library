import csv
import re

# 要整理wallets_with_consecutive_chars.csv文件并根据您的要求分类排序，我们需要编写一个脚本来读取文件内容，然后按照以下规则进行排序：

# 首先按照开头连号的存在与否进行排序，开头有连号的地址排在前面。
# 然后按照尾部连号的存在与否进行排序，尾部有连号的地址排在开头无连号地址的前面。
# 最后，按照连号的数字或字符进行分类（0-9, a-b）。

# 这个脚本首先定义了一个排序函数sort_key，用于根据地址的开头和尾部是否存在连号来确定每行的权重。然后，它读取原始的 CSV 文件，使用sort_key函数对行进行排序，并将排序后的结果写入一个新的 CSV 文件wallets_sorted.csv。

# 请确保在运行此脚本前，wallets_with_consecutive_chars.csv文件位于与脚本相同的目录下。执行后，您将在同一目录下得到一个新的已排序的 CSV 文件wallets_sorted.csv。

def sort_key(row):
    address, mnemonic = row
    # 检查开头连号
    head_match = re.search(r'^0x([0-9a-b])\1{4,}', address.lower())
    # 检查尾部连号
    tail_match = re.search(r'([0-9a-b])\1{4,}$', address.lower())

    # 开头连号的权重最高
    if head_match:
        head_weight = 1
    else:
        head_weight = 0

    # 尾部连号的权重次之
    if tail_match:
        tail_weight = 1
    else:
        tail_weight = 0

    # 返回排序键
    return (head_weight, tail_weight, address)

# 读取CSV文件
with open('wallets_with_consecutive_chars.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    headers = next(reader)  # 跳过标题行
    rows = sorted(list(reader), key=sort_key, reverse=True)

# 将排序后的数据写回到一个新的CSV文件
with open('wallets_sorted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print("排序完成，结果已保存到 wallets_sorted.csv")
