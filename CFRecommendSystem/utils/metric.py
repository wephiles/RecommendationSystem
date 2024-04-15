# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/28 028 13:55
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : RecSys/metric.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import math
from recommender.user_cf import UserCF


class Metric(object):
    """评价指标类。"""

    def __init__(self):
        pass

    @staticmethod
    def mae(records: list):
        """
        列表records存放用户评分数据，令records[i] = [u,i,rui,pui]，其中rui是用户u对物品i的实际评分，
        pui是算法预测出来的用户u对物品i的评分
        Args:
            records (list):[[u,i,rui,pui], [u,i,rui,pui], [u,i,rui,pui], ...]

        Returns:

        """
        sum_ = 0
        for item in records:
            _, _, real_record, forcast_record = item
            sum_ += (real_record - forcast_record) ** 2
        return math.sqrt(sum_) / float(len(records))

    @staticmethod
    def rmse(records):
        """
        列表records存放用户评分数据，令records[i] = [u,i,rui,pui]，其中rui是用户u对物品i的实际评分，
        pui是算法预测出来的用户u对物品i的评分
        Args:
            records (list):[[u,i,rui,pui], [u,i,rui,pui], [u,i,rui,pui], ...]

        Returns:

        """
        sum_ = 0
        for item in records:
            _, _, real_record, forcast_record = item
            sum_ += abs(real_record - forcast_record)
        return sum_ / float(len(records))

    @staticmethod
    def precision(recommends, test_set):
        """

        Args:
            recommends ():
            test_set (): 测试集。

        Returns:

        """
        union_n = 0
        user_sum = 0
        for user, items in recommends.items():
            recommend_set = set(items)
        pass

    @staticmethod
    def recall(self):
        pass

    @staticmethod
    def coverage(self):
        pass

    @staticmethod
    def popularity(self):
        pass

# --END--
