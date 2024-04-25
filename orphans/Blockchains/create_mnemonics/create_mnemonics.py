# Create Mnemonics
from mnemonic import Mnemonic
from datetime import datetime

COUNT = 10

def create_mnemonics(strength=128):
    mnemonic = Mnemonic("english")
    return mnemonic.generate(strength)

if __name__ == "__main__":
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    with open(f"mnemonics{current_time}.txt", "w") as f:
        for i in range(COUNT):
            mnemonic = create_mnemonics()
            f.write(f"{mnemonic}\n")
            print(f"{i+1}. {mnemonic}")
            