from mnemonic import Mnemonic
from datetime import datetime
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

COUNT = 10

def create_mnemonics(strength=128):
    mnemonic = Mnemonic("english")
    return mnemonic.generate(strength)

if __name__ == "__main__":
    # 初始化 Word 文档
    doc = Document()
    doc.styles['Normal'].font.name = 'Nimbus Mono PS'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Nimbus Mono PS')

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    with open(f"mnemonics{current_time}.txt", "w") as f:
        for i in range(COUNT):
            mnemonic = create_mnemonics()
            f.write(f"{mnemonic}\n")
            print(f"{i+1}. {mnemonic}")
            # 将每个助记词添加到 Word 文档
            para = doc.add_paragraph(f"{i+1}. {mnemonic}")
            para.style.font.size = Pt(12)  # 设置字体大小

    # 保存 Word 文档
    doc.save(f"mnemonics{current_time}.docx")
