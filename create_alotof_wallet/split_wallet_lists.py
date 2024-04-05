import csv

# 定义文件名
filename = 'wallets.csv'

# 获取行数
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    row_count = sum(1 for row in reader)

# 计算每个分割文件应该包含的行数
rows_per_file = row_count // 10 + (1 if row_count % 10 else 0)

# 初始化变量
current_file_index = 1
current_line_count = 0
current_file = open(f'split_{current_file_index}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(current_file)

# 逐行读取和写入
with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        writer.writerow(row)
        current_line_count += 1
        if current_line_count >= rows_per_file:
            current_file.close()
            current_file_index += 1
            if current_file_index <= 10:  # 防止创建多余的文件
                current_file = open(f'split_{current_file_index}.csv', 'w', newline='', encoding='utf-8')
                writer = csv.writer(current_file)
                current_line_count = 0

# 关闭最后一个文件
if not current_file.closed:
    current_file.close()
