# coding:utf-8
from Src.Algorithm.AbstractHeightFitting import AbstractFitting
from numpy.linalg import pinv
import numpy as np
from Src.DataProcess.DataProcessingAnalysis import DataProcessing


class PlaneFit(AbstractFitting):
    """
    平面拟合法 f = a0 + a1x + a2y
    """
    def __init__(self, basicData, number_known):
        self.__data = PlaneFit.__ctor(basicData)
        self.__known_point = self.__data[:number_known]
        self.__check_point = self.__data[number_known:]

        self.number = number_known

    @staticmethod
    def __ctor(basic_data):
        if basic_data is None:
            return
        if len(basic_data[0]) > 3:
            return [(item[0], item[1], item[4]) for item in basic_data]
        else:
            return [(item[0], item[1], item[2]) for item in basic_data]

    def CalcResidual(self, hf):
        pass

    def CalcAllPointHf(self):
        # A
        A = []
        for item in self.__known_point:
            A.append([1, item[0], item[1]])
        # L
        L = [item[2] for item in self.__known_point]  # 10 * 1
        a = np.array(A).reshape(self.number, 3)  # 10 * 3
        at = a.transpose()  # 3 * 10
        X = np.matmul(pinv(np.matmul(at, a)), np.matmul(at, np.array(L)))
        return [np.matmul(np.array([1, item[0], item[1]]), X) for item in self.__check_point]


if __name__ == '__main__':
    src = DataProcessing('../../Data/gps_data_1.txt')
    basicData = src.Data
    p = PlaneFit(basicData[0], 10)
    e = p.CalcAllPointHf()
    print(e)
