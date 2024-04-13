from mnemonic import Mnemonic
from datetime import datetime
from docx import Document
from docx.shared import Pt, Cm
from docx.oxml.ns import qn
from docx.enum.text import WD_LINE_SPACING

COUNT = 10

def create_mnemonics(strength=128):
    mnemonic = Mnemonic("english")
    return mnemonic.generate(strength)

if __name__ == "__main__":
    # 初始化 Word 文档
    doc = Document()
    # doc.styles['Normal'].font.name = 'Nimbus Mono PS'
    # doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Nimbus Mono PS')
    
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(1)
        section.left_margin = Cm(1)
        section.right_margin = Cm(1)

    # 设置字体和行间距
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Nimbus Mono PS'
    font.size = Pt(10)

    # 设置段落的行间距
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE # 单倍行距

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')

    for i in range(COUNT):
        mnemonic = create_mnemonics()
        print(f"{i+1}. {mnemonic}")
        # 将每个助记词添加到 Word 文档
        para = doc.add_paragraph(f"{i+1}. {mnemonic}")
        para.style.font.size = Pt(12)  # 设置字体大小

    # 保存 Word 文档
    doc.save(f"mnemonics{current_time}.docx")
