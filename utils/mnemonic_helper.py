from mnemonic import Mnemonic

mnemo = Mnemonic("english")

def get_12_seed():
    mnemonic_words = mnemo.generate(strength=128)
    return mnemonic_words

def get_15_seed():
    mnemonic_words = mnemo.generate(strength=160)
    return mnemonic_words

def get_18_seed():
    mnemonic_words = mnemo.generate(strength=192)
    return mnemonic_words

def get_21_seed():
    mnemonic_words = mnemo.generate(strength=224)
    return mnemonic_words

def get_24_seed():
    mnemonic_words = mnemo.generate(strength=256)
    return mnemonic_words
