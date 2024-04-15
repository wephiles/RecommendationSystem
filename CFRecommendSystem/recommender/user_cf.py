# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/28 028 11:16
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : CFRecSys/user_cf.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import math
import sys
from collections import defaultdict
from operator import itemgetter

from utils.utils import load_data, save_data


class UserCF(object):
    """基于用户的协同过滤算法

    - 基于用户的协同过滤算法（User-based Collaborative Filtering）是一种推荐系统算法，它的核心思想是通过分析用户之间的相似性
    来预测用户可能感兴趣的物品。这种算法假设如果两个用户在过去对一系列物品的评分或行为表现出了相似的模式，那么他们在未来对未评
    分物品的偏好也会相似。

    - 算法步骤
    1. 用户相似度计算:
    首先，算法需要计算用户之间的相似度。这通常通过比较用户对相同物品的评分来实现。常用的相似度度量方法包括皮尔逊相关系数
    （Pearson correlation coefficient）、余弦相似度（Cosine similarity）和杰卡德相似系数（Jaccard similarity）等。
    2. 找到相似用户:
    对于目标用户，算法会找到一组与其相似度最高的其他用户，这组用户被称为“邻居”（neighbors）。
    3. 生成推荐:
    然后，算法会分析这些邻居用户对物品的评分，找出他们共同喜欢的物品。这些物品被认为是目标用户可能感兴趣的。
    通常，算法会根据邻居用户的评分和相似度对推荐物品进行加权，以生成一个推荐列表。
    4. 推荐排序:
    最后，算法会根据加权评分对推荐物品进行排序，并向目标用户推荐评分最高的物品。

    - 缺点:
    1. 冷启动问题：对于新用户或新物品，由于缺乏足够的评分数据，算法可能无法提供有效的推荐。
    2. 稀疏性问题：在大型系统中，用户-物品交互矩阵通常非常稀疏，这可能导致推荐质量下降。
    3. 计算成本：计算用户之间的相似度可能需要大量的计算资源，尤其是在用户数量很大的情况下。

    - 如何使用: 你可以根据以下实例代码运行算法，前提是你需要准备好数据集。
        ```
        # 首先，你要导入UserCF算法类并实例化:
        import user_cf
        uf = user_cf.UserCF()
        ```
    """

    def __init__(self):
        self.train_data = None
        self.sim_matrix_path = r"./data/similarity_matrix.pkl"
        self.train = None
        self.user_similarity_matrix = None

    def calculate_user_similarity(self):
        """
        计算用户相似度矩阵。
        Returns:
            ...
        """
        # build inverse table for item_users
        item_users = dict()
        for user, items in self.train.items():
            for item in items:
                item_users.setdefault(item, set())
                item_users[item] = user
        # item_users = {item1: {user1, user2, ...}, item2: {user1, user2, ...}, ...}

        # calculate co-rated items between users
        co_related_dict = dict()
        N = defaultdict(int)  # 每个用户所交互过的项目总数。
        # N = {user1: number_items_1, user2: number_items_2, ...}
        for i, users in item_users.items():
            for u in users:
                N[u] += 1
                for v in users:
                    if u == v:
                        continue
                    co_related_dict.setdefault(u, defaultdict(int))
                    co_related_dict[u][v] += 1

        # co_related_dict =
        #     {user1: {user4: item_nums, item10: item_nums},
        #     user2:{user8: item_nums, item10: item_nums},
        #     ...
        # }

        # calculate final similarity matrix
        user_similarity_matrix = dict()
        for user_u, related_users in co_related_dict.items():
            for user_v, related_items_num in related_users.items():
                user_similarity_matrix.setdefault(user_u, defaultdict(int))
                user_similarity_matrix[user_u][user_v] = related_items_num / math.sqrt(N[user_u] * N[user_v])
        self.user_similarity_matrix = user_similarity_matrix
        return user_similarity_matrix

    def train(self, train_data, sim_matrix_path=r""):
        """
        训练模型。
        Args:
            train_data ():
            sim_matrix_path ():

        Returns:

        """
        if train_data is None:
            train_data = train_data
        if sim_matrix_path == r"":
            sim_matrix_path = self.sim_matrix_path
        self._init_train(train_data)
        print("----------------- train model ... -----------------")
        try:
            print("loading user similarity matrix ...", file=sys.stderr)
            self.user_similarity_matrix = load_data(file_path=sim_matrix_path)
            print("successfully loaded user similarity matrix.", file=sys.stderr)
        except FileExistsError:
            print("Failed to load user similarity matrix, try to calculate user similarity matrix ...", file=sys.stderr)
            self.user_similarity_matrix = self.calculate_user_similarity()
            print("successfully calculated user similarity matrix.", file=sys.stderr)
        print("save similarity matrix data ...", file=sys.stderr)
        save_data(file_path=sim_matrix_path, data=train_data)
        print("successfully saved similarity matrix data.", file=sys.stderr)
        print("----------------- successfully trained model ... -----------------")

    def _init_train(self, train_data=None):
        """
        初始化训练数据。
        Args:
            train_data ():

        Returns:

        """
        if train_data is None:
            train_data = self.train_data
        print("initialize train data ...", file=sys.stderr)
        self.train = dict()
        for user, item, _ in train_data:
            self.train.setdefault(user, set())
            self.train[user].add(item)
        print("successfully initialized train data.", file=sys.stderr)

    def recommend(self, user_id, n, k):
        """
        推荐。
        Args:
            user_id (str/int): 用户id
            n (int): 推荐n个商品
            k (int):  查找最相似的用户个数。

        Returns:
            dictionary object {物品: 相似性打分情况}
        """
        print("recommendation system is running ...")
        # train = {user1: {item1, item2, ...}, user2: {item3, item4, ...}}
        related_items = self.train.get(user_id, set)
        # related_items(和user_id相关的) = {item1 , item2, ...}
        recommends = dict()
        for user_v, similarity in sorted(
                # user_similarity_matrix =
                #     {user1: {user4: item_nums, item10: item_nums},
                #     user2:{user8: item_nums, item10: item_nums},
                #     ...
                # }
                self.user_similarity_matrix.get(user_id, dict).items(),  # {item1: num1, ...}
                key=itemgetter(1),  # 以和用户user_id相关的相似性打分情况排序
                reverse=True  # 从大到小拍，以便于选取前k个
        )[:k]:
            for item in self.train[user_v]:  # 遍历所有用户
                if item in related_items:
                    continue
                recommends.setdefault(item, 0.)
                recommends[item] += similarity  # 物品的所有打分信息
        return dict(
            sorted(recommends.items(), key=itemgetter(1), reverse=True)[:n]
        )

    def recommend_users(self, users, n, k):
        """
        在测试集上推荐，给用户推荐项目。
        Args:
            users (list):
            n ():
            k ():

        Returns:
            {用户: [项目]}
        """
        recommends = dict()
        for user in users:
            user_recommends = list(self.recommend(user, n=n, k=k))
            recommends[user] = user_recommends
        return recommends

# --END--
