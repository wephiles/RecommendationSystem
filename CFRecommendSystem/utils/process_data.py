# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/28 028 11:19
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : CFRecSys/process_data.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import sys
import random


class ProcessData(object):

    def __init__(self):
        self.file_path = r"./data/ml-100k/u.data"
        self.ratio_split = 0.8

    def load_data(self, file_path=r""):
        """加载数据。 -- 一个生成器函数。

        Args:
            file_path (str): 需要被加载文件的文件路径。

        Returns: string data

        """
        if file_path == r"":
            file_path = self.file_path
        try:
            with open(file_path, mode="r") as fp:
                for line in fp:
                    yield line
        except FileExistsError as e:
            print("File was not found, please check the path of file. ", file=sys.stderr)
            print(e)

    def split_data(self, file_path=r"", ratio_split=0., seed=1):
        """

        Args:
            file_path ():
            ratio_split ():
            seed ():

        Returns:

        """
        if file_path == r"":
            file_path = self.file_path
        if ratio_split <= 0. or ratio_split >= 1.:
            ratio_split = self.ratio_split
        train_set, test_set = [], []
        random.seed(seed)
        for line in self.load_data(file_path):
            user_id, movie_id, rating, time_stamp = line.strip().split("::")
            if random.random() <= ratio_split:
                train_set.append((int(user_id), int(movie_id), int(rating), int(time_stamp)))
            else:
                test_set.append((int(user_id), int(movie_id), int(rating), int(time_stamp)))
        return train_set, test_set

    def get_all_items(self, file_path=r""):
        """

        Args:
            file_path (str): 文件路径。

        Returns :
            set 所有电影物品信息。
        """
        if file_path == r"":
            file_path = self.file_path

        items_dict = set()
        for line in self.load_data(file_path):
            _, movie_id, _, _ = line.strip().split("::")
            items_dict.add(movie_id)
        return items_dict

# --END--
