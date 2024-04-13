import csv
import re
from itertools import groupby

# 每换一个字符以及一种判断模式（如：开头，结尾，其他）则换行，

# 要实现这个需求，我们需要调整排序逻辑，并在写入新文件时根据字符和判断模式（开头、结尾、其他）进行换行。我们将为每个地址定义一个分类标签，然后根据这个标签进行分组和排序。

# 这个脚本首先通过classify函数为每个地址分配一个类别（头部连号、尾部连号或其他）。然后，它使用sort_key函数对这些分类进行排序。最后，它使用groupby函数按类别分组，并在每组后添加一个空行，然后将这些数据写入新的CSV文件。

# 执行此脚本后，您将得到一个名为wallets_sorted.csv的文件，其中包含根据地址的特定连号模式排序和分组的钱包地址和助记词，每种模式的地址都由一个空行分隔。

def classify(row):
    address, mnemonic = row
    head_match = re.search(r'^0x([0-9a-b])\1{4,}', address.lower())
    tail_match = re.search(r'([0-9a-b])\1{4,}$', address.lower())

    if head_match:
        return ('head', head_match.group(1), address, mnemonic)
    elif tail_match:
        return ('tail', tail_match.group(1), address, mnemonic)
    return ('other', None, address, mnemonic)

def sort_key(item):
    category, char, address, mnemonic = item
    if category == 'head':
        return (0, char, address)
    elif category == 'tail':
        return (1, char, address)
    return (2, None, address)

# 读取CSV文件
with open('wallets_with_consecutive_chars.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    headers = next(reader)  # 跳过标题行
    classified_rows = sorted([classify(row) for row in reader], key=sort_key)

# 将排序和分类后的数据写入新的CSV文件
with open('wallets_sorted.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for key, group in groupby(classified_rows, key=lambda x: (x[0], x[1])):
        for item in group:
            _, _, address, mnemonic = item
            writer.writerow([address, mnemonic])
        writer.writerow([])  # 在每个分类后添加空行

print("排序完成，结果已保存到 wallets_sorted.csv")
