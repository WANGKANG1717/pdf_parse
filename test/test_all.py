# -*- coding: utf-8 -*-
# @Date     : 2023-12-13 10:33:21
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : test_all.py
# @Brief    : 测试所有包
# Copyright 2023 WANGKANG, All Rights Reserved.

# 性能（生成时间）、解析样式、表格的解析
import os
import time
from pdfminer.high_level import extract_text
import pdfplumber
import fitz  # imports the pymupdf library
import typing

from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit import SimpleTextExtraction


root_dir = "./pdf"
out_dir = "./pdf_out"
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def save_text(text, file_name, package_name):
    with open(
        os.path.join(out_dir, f"{file_name.removesuffix('.pdf')}_{package_name}.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(text)


def test_pdfminer():
    start_time = time.time()
    package_name = "pdfminer"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_names = os.listdir(root_dir)

    for file_name in file_names:
        text = extract_text(os.path.join(root_dir, file_name))
        # print(text)
        save_text(text, file_name, package_name)

    end_time = time.time()
    print(f"{package_name} -- 所用时间:{end_time - start_time: 0.2f}s")


def test_pdfplumber():
    start_time = time.time()
    package_name = "pdfplumber"
    file_names = os.listdir(root_dir)

    for file_name in file_names:
        text = ""
        with pdfplumber.open(os.path.join(root_dir, file_name)) as pdf:
            for idx, page in enumerate(pdf.pages):
                text += page.extract_text() + "\n"
                # print(page.extract_tables())
                # img = page.to_image()
                # img.draw_rects(page.extract_words())
                # # img.draw_rects(page.extract_text_lines())
                # img.save(f"./images/extract_words_page{idx}.png", format="PNG")
        save_text(text, file_name, package_name)

    end_time = time.time()
    print(f"{package_name} -- 所用时间:{end_time - start_time: 0.2f}s")


def test_PyMuPDF():
    start_time = time.time()
    package_name = "PyMuPDF"
    file_names = os.listdir(root_dir)

    for file_name in file_names:
        text = ""

        doc = fitz.open(os.path.join(root_dir, file_name))  # open a document
        for page in doc:  # iterate the document pages
            text += page.get_text() + "\n"  # get plain text encoded as UTF-8

        save_text(text, file_name, package_name)

    end_time = time.time()
    print(f"{package_name} -- 所用时间:{end_time - start_time: 0.2f}s")


def test_borb():
    start_time = time.time()
    package_name = "borb"
    file_names = os.listdir(root_dir)

    for file_name in file_names:
        text = ""

        doc: typing.Optional[Document] = None
        l: SimpleTextExtraction = SimpleTextExtraction()
        with open(os.path.join(root_dir, file_name), "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        # check whether we have read a Document
        assert doc is not None

        data = l.get_text_from_pdf(doc)
        for sub_text in data.values():
            text += sub_text + "\n"

        save_text(text, file_name, package_name)

    end_time = time.time()
    print(f"{package_name} -- 所用时间:{end_time - start_time: 0.2f}s")


if __name__ == "__main__":
    pass
    test_pdfminer()
    test_pdfplumber()
    test_PyMuPDF()
    test_borb()
