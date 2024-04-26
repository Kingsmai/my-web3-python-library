import csv
import re
from itertools import groupby

# 再根据他们的特征进行排序，连号越多越靠前

# 要实现这个需求，我们需要进一步细化排序逻辑，让连号更多的地址排在前面。这涉及到在classify函数中记录连号的长度，并在sort_key函数中使用这个长度进行排序。

# 以下是更新后的脚本，它会根据连号的特征（位置和长度）进行排序：

# 这个脚本现在会根据连号的位置、字符以及长度对地址进行分类和排序。在classify函数中，除了标记连号的位置和字符外，还记录了连号的长度。然后在sort_key函数中，使用这些信息进行排序，优先考虑连号位置（头部连号优先于尾部连号），然后是连号字符，最后是连号长度（越长越优先）。

# 执行此脚本后，您将得到一个名为wallets_sorted_grouped.csv的文件，其中包含根据连号特征排序和分组的钱包地址和助记词，每种模式的地址组之间用空行分隔。

# 101962200

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
