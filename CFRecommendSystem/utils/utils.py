# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/28 028 13:17
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : RecSys/utils.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import os
import pickle


class Utils(object):
    """工具类。"""

    def __init__(self):
        self.file_path = r"./data/ml-100k/u.data"
        self.data = None

    def save_data(self, file_path=r"", data=None):
        """

        Args:
            file_path (str): 要保存到的文件路径。
            data (bytes): 流式文件。

        Returns:
            bool
        """
        if data is None:
            raise Exception("No data can be saved!")
        if file_path == r"":
            file_path = self.file_path
        parent_path = file_path[:file_path.rfind("/")]
        if not os.path.exists(parent_path):
            os.mkdir(parent_path)
        with open(file_path, "wb") as fp:
            pickle.dump(data, fp)
        return True

    def load_data(self, file_path=r""):
        """

        Args:
            file_path (str): 数据存储路径。

        Returns:
            bytes 字节流数据
        """
        if file_path == r"":
            file_path = self.file_path
        with open(file_path, "rb") as fp:
            data = pickle.load(fp)
        return data

    def load_text(self, file_path=r"", skip_row_list=None, skip_rows=0):
        """

        Args:
            file_path (str): 文件路径
            skip_row_list (list[int]): 跳过某几行
            skip_rows (int): 跳过前面几行

        Returns:
            生成器函数。
        """
        if file_path == r"":
            file_path = self.file_path
        if skip_row_list is None:
            skip_row_list = []
        with open(file_path, "r", encoding="utf-8") as fp:
            for i, line in enumerate(fp):
                if i <= skip_rows or i in skip_row_list:
                    continue
                yield line

# --END--
