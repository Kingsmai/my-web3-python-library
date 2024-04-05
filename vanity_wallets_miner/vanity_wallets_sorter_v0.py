import csv
import re
from itertools import groupby

def classify(row):
    address, mnemonic = row
    # 查找开头和结尾的连号
    head_match = re.search(r'^0x([0-9a-b])\1{4,}', address.lower())
    tail_match = re.search(r'([0-9a-b])\1{4,}$', address.lower())

    if head_match:
        return ('head', head_match.group(1), len(head_match.group(0)) - 2, address, mnemonic)
    elif tail_match:
        return ('tail', tail_match.group(1), len(tail_match.group(0)), address, mnemonic)
    return ('other', None, 0, address, mnemonic)

def sort_key(item):
    # 排序优先级：类别（头部连号>尾部连号>其他）、连号字符、连号长度（降序）、地址
    category, char, length, address, _ = item
    return (0 if category == 'head' else 1 if category == 'tail' else 2, char, -length, address)

# 读取CSV文件
with open('wallets_with_consecutive_chars.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    headers = next(reader)  # 跳过标题行
    classified_rows = sorted([classify(row) for row in reader], key=sort_key)

# 将排序和分类后的数据写入新的CSV文件
with open('wallets_sorted_grouped.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for key, group in groupby(classified_rows, key=lambda x: (x[0], x[1])):
        for item in group:
            _, _, _, address, mnemonic = item
            writer.writerow([address, mnemonic])
        writer.writerow([])  # 在每个分类后添加空行

print("排序完成，结果已保存到 wallets_sorted_grouped.csv")
