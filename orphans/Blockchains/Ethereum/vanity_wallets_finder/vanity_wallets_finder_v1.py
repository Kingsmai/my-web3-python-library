import csv

for i in range(8):
    with open(f"out/wallet/wallets_with_consecutive_chars_{i + 1}.csv", "r") as f:
        reader = csv.reader(f)
        for line in reader:
            if line[0].endswith('8888888'):
                with open(f"out/wallet/wallets_ends_with_7_8.csv", "a") as out:
                    writer = csv.writer(out)
                    writer.writerow(line)
            if line[0].endswith('7777777'):
                with open(f"out/wallet/wallets_ends_with_7_7.csv", "a") as out:
                    writer = csv.writer(out)
                    writer.writerow(line)
