# -*- coding: utf-8 -*-
# @Date     : 2023-12-11 18:28:43
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : main.py
# @Brief    : 解析txt文件
# Copyright 2023 WANGKANG, All Rights Reserved.
import re


class ParseText:
    MATCH_PAGE_HEADER = r"(第[\d]+页 共[\d]+页)|(目 次)"
    MATCH_CATALOG = r"([\d. ]*[、\u4e00-\u9fa5]+) [.]+[ ]*[\d]+$"
    MATCH_SUB_TITLE_LEVEL2 = r"(^[\d]+[.][\d]+ .+)"  # [.][\d]+ 向后累加，即可得到多级子标题的正则表达式

    def __init__(self, path) -> None:
        self.raw_text = None
        self.text = None
        self.path = path
        self.catalog_names = []  # 目录
        self.catalog_content = {}  # 一级目录对应的内容
        self.read_text()

    def read_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
            self.text = self.raw_text

    def parseText(self):
        self.remove_blank()
        self.remove_page_header()
        self.split_chapter_block()
        self.get_catalog_content()
        self.split_sub_title_level2_name()

        return self.text

    def remove_blank(self):
        cnt = 0
        while True:
            self.text = self.text.strip().replace("  ", " ").replace("\n\n", "\n")
            cnt += 1
            if cnt >= 10:
                break

    def remove_page_header(self):
        lines = self.text.split("\n")
        tmp = []
        for line in lines:
            line = line.strip()
            if re.search(self.MATCH_PAGE_HEADER, line) is None:
                tmp.append(line)
        self.text = "\n".join(tmp)

    def split_chapter_block(self):
        lines = self.text.split("\n")
        self.catalog_names = []  # 提取的目录标题
        tmp = []
        for line in lines:
            line = line.strip()
            if re.search(self.MATCH_CATALOG, line):
                self.catalog_names.append(re.search(self.MATCH_CATALOG, line).group(1))
            else:
                tmp.append(line)
        self.text = "\n".join(tmp)
        print(self.catalog_names)

    def get_catalog_content(self):
        text = self.text.split("\n", 1)[1]
        # print(text)
        for idx in range(len(self.catalog_names)):
            if (idx + 1) > len(self.catalog_names) - 1:
                break
            current_catalog_name = self.catalog_names[idx]
            next_catalog_name = self.catalog_names[idx + 1]
            content, text = text.split(next_catalog_name, 1)
            content = content.strip()
            text = text.strip()
            self.catalog_content[current_catalog_name] = content

        last_catalog_name = self.catalog_names[len(self.catalog_names) - 1]
        self.catalog_content[last_catalog_name] = text.strip()
        # print(self.catalog_content)
        # for name, content in self.catalog_content.items():
        #     print(name)
        #     print(content)
        #     print("*" * 50)

    def split_sub_title_level2_name(self):
        for name, content in self.catalog_content.items():
            lines = content.split("\n")
            sub_title = []
            for line in lines:
                line = line.strip()
                if re.search(self.MATCH_SUB_TITLE_LEVEL2, line):
                    sub_title.append(
                        re.search(self.MATCH_SUB_TITLE_LEVEL2, line).group(1)
                    )
            print(content)
            print(sub_title)
            print("*" * 50)


if __name__ == "__main__":
    app = ParseText("./tmp.txt")
    text = app.parseText()
    # print(text)
