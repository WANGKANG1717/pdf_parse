import re
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTText, LTChar, LTAnno, LTTextLine


domain_1 = "系统支架结构设计规范"
topic_name = ""
facet_1 = ""
section_2 = 0  # 章节号


def parse_line_layout(layout):
    """解析页面内容，一行一行的解析"""
    pattern = r"\d+\s+([\w\s]+)"
    pattern1 = r"\d+\.\d+\s+([\w\s]+)"
    pattern2 = r"\d+\.\d+\.\d+\s+([\w\s]+)"
    pattern3 = r"\d+\.\d+\.\d+\.\d+\s+([\w\s]+)"
    pattern4 = r"\s+([\w\s]+)"
    pattern5 = r"[，\。\？\！]"
    b = re.findall(pattern5, "支架结构的设计界面主要包括：支架与所需要安装的系统连接界面、支架与所依附的机体")

    with open("./tmp.txt", "a", encoding="utf-8") as f:
        for textbox in layout:
            if isinstance(textbox, LTTextBox) or isinstance(textbox, LTTextLine):
                for char in textbox:
                    # print("坐标 x:", char.bbox[0], "y:", char.bbox[3], " ||| ", char.get_text().strip(), )
                    a = char.get_text().strip()
                    f.write(a + "\n")


if __name__ == "__main__":
    fp = open("./JY结构通用设计要求.pdf", "rb")
    parser = PDFParser(fp)  # 用文件对象来创建一个pdf文档分析器
    doc: PDFDocument = PDFDocument(parser)  # 创建pdf文档

    rsrcmgr = PDFResourceManager()  # 创建PDF，资源管理器，来共享资源
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释其对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 处理文档对象中每一页的内容
    # doc.get_pages() 获取page列表
    # 循环遍历列表，每次处理一个page的内容
    # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_line_layout(layout)
        # topic_name, section_2 = parse_line_layout(layout, topic_name, section_2, facet_1)  # 解析句子
