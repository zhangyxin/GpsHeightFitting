# coding:utf-8
from Src.Algorithm.AbstractHeightFitting import AbstractFitting
from Src.DataProcess.DataProcessingAnalysis import DataProcessing
import math
import numpy as np
from numpy.linalg import pinv


class Polyhedral(AbstractFitting):
    """
    多面函数曲面拟合
    """
    def __init__(self, basic_data, known_number):
        data = Polyhedral.__ctor(basic_data)
        self.__known = data[:known_number]
        self.__unknown = data[known_number:]
        # 已知点个数
        self.__n = known_number
        self.__m = self.__n  # 核函数核心点个数
        # 平滑因子
        self.gm = 27000

    @staticmethod
    def __ctor(basic_data):
        if basic_data is None:
            return
        if len(basic_data[0]) > 3:
            return [(item[0], item[1], item[4]) for item in basic_data]
        else:
            return [(item[0], item[1], item[2]) for item in basic_data]

    def __ctor_ql(self) -> tuple:
        """
        构造Q系数矩阵 L常数矩阵
        """
        Q = []
        L = []

        for i in range(0, self.__n):
            # Q 矩阵 shape = n * m
            Q.append([self.__qz(self.__known[i][0], self.__known[i][1], self.__known[j][0], self.__known[j][1])
                      for j in range(0, self.__m)])
            # L 矩阵 shape = n * 1
            L.append(self.__known[i][2])

        return Q, L

    def __qz(self, xi, yi, xj, yj):
        """
        二次核函数 正双曲面函数
        """
        return math.pow(math.pow(xi - xj, 2) + math.pow(yi - yj, 2) + math.pow(self.gm, 2), 0.5)

    def __qf(self, xi, yi, xj, yj):
        """
        二次核函数 倒双曲面函数
        """
        return 1 / self.__qz(xi, yi, xj, yj)

    def CalcAllPointHf(self):
        # 计算 Q, L
        q, l = self.__ctor_ql()
        # 计算 beta
        L = np.array(l, dtype=np.float).reshape(self.__n, 1)
        Q = np.array(q, dtype=np.float).reshape(self.__n, self.__m)
        QT = Q.transpose()

        if self.__m == self.__n:
            beta = np.matmul(pinv(Q), L)
        else:
            qtq = np.matmul(QT, Q)
            qtl = np.matmul(QT, L)
            beta = np.matmul(pinv(qtq), qtl)

        # 计算所有未知点的高程异常
        return [self.__calc_single_point(beta, item[0], item[1]) for item in self.__unknown]

    def __calc_single_point(self, beta, x, y):
        """
        计算单个未知点的高程异常
        """
        c = [self.__qz(x, y, self.__known[i][0], self.__known[i][1]) for i in range(0, self.__m)]
        C = np.array(c).reshape(1, self.__m)
        return np.matmul(C, beta)[0][0]

    def CalcResidual(self, hf):
        pass


if __name__ == '__main__':
    src = DataProcessing('../../Data/gps_data_1.txt')
    basicData = src.Data
    p = Polyhedral(basicData[0], 10)
    e = p.CalcAllPointHf()
    print(e)
