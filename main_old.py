# -*- coding: utf-8 -*-
# @Date     : 2023-12-11 18:28:43
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : main.py
# @Brief    : 解析txt文件
# Copyright 2023 WANGKANG, All Rights Reserved.
import os
import re
import json
import sys


class ParseText:
    MATCH_PAGE_HEADER = r"(第[\d]+页 共[\d]+页)|(目 次)"
    MATCH_PARSE_START_TAG = r"(^前 言$)"  # 用来区分从哪里开始解析,可以使用|添加多个条件

    def __init__(self, path) -> None:
        self.raw_text = None
        self.text = None
        self.path = path
        self.content_tree = {}  # 使用字典构建的树结构

        self.read_text()

    def read_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()
            self.text = self.raw_text

    def get_match_title_levels_of_n(self, n):
        return r"(^[\d]+{} .+)".format(r"[.][\d]+" * (n - 1))

    def parseText(self):
        self.remove_blank()
        self.remove_page_header()
        self.remove_catalog()
        # self.debug()
        self.content_tree = self.parse_text_recursion(self.text, "root", 1)

    def remove_blank(self):
        self.text = re.sub(" +", " ", self.text, flags=re.M)
        self.text = re.sub("\x0c", "", self.text, flags=re.M)
        self.text = re.sub("\n[\n ]*", "\n", self.text, flags=re.M)

    def remove_page_header(self):
        lines = self.text.split("\n")
        tmp = []
        for line in lines:
            line = line.strip()
            if re.search(self.MATCH_PAGE_HEADER, line) is None:
                tmp.append(line)
        self.text = "\n".join(tmp)

    def remove_catalog(self):
        # print(self.text)
        # print(re.search(self.MATCH_PARSE_START_TAG, self.text, re.M).group(1))
        self.text = "".join(
            re.split(self.MATCH_PARSE_START_TAG, self.text, 1, re.M)[1:]
        )
        self.text = self.text.replace("前 言", "0 前言", 1)

    def parse_text_recursion(self, text, cur_title, level):
        tmp_tree: list | dict = None
        match_rule = self.get_match_title_levels_of_n(level)
        if level == 1:
            tmp = re.findall(match_rule, text, re.M)
            # print(res)
            sub_titles = []
            for i in range(len(tmp)):
                j = int(tmp[i].split(" ", 1)[0])
                if i == j:
                    sub_titles.append(tmp[i])
        else:
            sub_titles = re.findall(match_rule, text, re.M)
            if not sub_titles:
                return text
        print(f"level{level} - {cur_title}: {sub_titles}")
        title_content = self.split_text_by_title(text, sub_titles)
        if isinstance(title_content, list):
            redundant_content, title_content = title_content[0], title_content[1]
            tmp_tree__ = {}
            for title in sub_titles:
                tmp_tree__[title] = self.parse_text_recursion(
                    title_content[title], title, level + 1
                )
            tmp_tree = [redundant_content, tmp_tree__]

        elif isinstance(title_content, dict):
            tmp_tree = {}
            for title in sub_titles:
                tmp_tree[title] = self.parse_text_recursion(
                    title_content[title], title, level + 1
                )

        return tmp_tree

    def split_text_by_title(self, text, titles):
        """这里有一个特殊情况，上级标题和当前标题之间还有一段内容，这种情况需要进行特殊判断"""
        title_content = {}
        redundant_content, text = text.split(titles[0], 1)

        # 也就是上级标题和当前标题之间没有多余的文字
        for idx in range(len(titles)):
            if (idx + 1) > len(titles) - 1:
                break
            current_title_name = titles[idx]
            next_title_name = titles[idx + 1]
            content, text = text.split(next_title_name, 1)
            content = content.strip()
            text = text.strip()
            title_content[current_title_name] = content

        last_title_name = titles[-1]
        title_content[last_title_name] = text.strip()

        if not redundant_content.strip():
            return title_content
        else:
            return [redundant_content, title_content]

    def save_content_tree(self, path):
        json.dump(
            self.content_tree,
            open(path, "w", encoding="utf-8"),
            ensure_ascii=False,
        )

    def debug(self):
        tmp = {"1": self.text}
        print(tmp)
        with open("./tmp.txt", "w", encoding="utf-8") as f:
            f.write(self.text)


if __name__ == "__main__":
    root_dir = "./pdf_out"
    out_dir = "./pdf_parse"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_name = "test1_pdfplumber.txt"

    app = ParseText(os.path.join(root_dir, file_name))
    app.parseText()
    app.save_content_tree(
        os.path.join(out_dir, f"{file_name.removesuffix('.txt')}.json")
    )

    # text = "3.1 维修性 maintainability\n产品在规定的条件下和规定的时间内，按规定的程序和方法进行维修时，保持或恢复到规\n定状态的能力。"
    # print(text)
    # print(text.split("\n", 1)[1])
    # data = json.load(open("./pdf_parse/test1_pdfminer.json"))
    # text = data["3 术语和定义"]["3.1 维修性 maintainability"]
    # print(text)
    # print(text.split("\n", 1)[1])
