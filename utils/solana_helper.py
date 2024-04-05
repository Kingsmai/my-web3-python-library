# 一个用于比特币改进提案 (BIP) 相关工具的 Python 库。
# 在这个上下文中，它被用来处理与 BIP39（助记词）和 BIP44（钱包分层结构）相关的功能。
import bip_utils as bip


# 利用了 BIP39 和 BIP44 标准来从一个助记词生成一个 Solana 地址。
def get_solana_keys_from_mnemonic(mnemonic: str, account_idx: int = 0):
    # 助记词生成了一个种子。
    # Bip39SeedGenerator 类用于根据给定的助记词生成种子，
    # 而 .Generate("") 方法生成种子，传入的参数是密码短语，这里为空字符串。
    seed_bytes = bip.Bip39SeedGenerator(mnemonic).Generate("")

    # 使用生成的种子创建了一个 BIP44 主上下文。
    # bip.Bip44.FromSeed 方法接受种子和币种作为参数，
    # 这里指定了 Solana 作为币种。
    bip44_mst_ctx = bip.Bip44.FromSeed(seed_bytes, bip.Bip44Coins.SOLANA)
    
    # 进一步细化了路径，获取账户层上下文。
    # 在 BIP44 标准中，路径通常表示为 m / purpose' / coin_type' / account' / change / address_index。
    # 这里 Account(0) 指的是路径中的第一个账户。
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(account_idx)
    
    # 在 BIP44 路径中，改变层用于区分外部（用于接收资金）和内部（用于找零）地址。
    # 这里使用 CHAIN_EXT 表示外部链。
    bip44_chg_ctx = bip44_acc_ctx.Change(bip.Bip44Changes.CHAIN_EXT)
    
    # 计算并打印出 Solana 地址。bip44_chg_ctx.PublicKey().ToAddress() 会从公钥生成 Solana 地址。
    return bip44_chg_ctx.PublicKey().ToAddress()

if __name__ == "__main__":
    get_solana_keys_from_mnemonic("")
