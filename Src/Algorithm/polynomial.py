# -*- coding:utf-8 -*-
import numpy
from numpy.linalg import pinv
from Src.DataProcess import DataProcessingAnalysis
from Src.Algorithm.AbstractHeightFitting import AbstractFitting
import math


class Polynomial(AbstractFitting):
    """
    二次曲面拟合法
    """
    def __init__(self, basic_data, number_balance):
        """
        :param basic_data:原始GPS点数据
        :param number_balance: 参与拟合的点的数量
        """
        if basic_data is None:
            raise Exception('The imported data is NoneType!')
        self.__data = self.__ctor(basic_data)
        # 参与拟合的点
        self.__parameter_point = self.__data[:number_balance]
        # 参与检查的点
        self.__check_point = self.__data[number_balance:]
        # 参与拟合的点数量
        self.number = number_balance

    def __ctor(self, basic_data):
        if basic_data is None:
            return
        if len(basic_data[0]) > 3:
            return [[item[0], item[1], item[4]] for item in basic_data]
        else:
            return [[item[0], item[1], item[2]] for item in basic_data]

    def __str__(self):
        return "二次曲面拟合法"

    def __get_matrix_B(self):
        """
        构造系数矩阵 B
        ：:rtype None
        """
        # 1 x y x2 xy y2
        B = [[1, item[0], item[1], item[0] * item[0], item[0] * item[1], item[1] * item[1]] for item in self.__parameter_point]
        return B

    def __get_matrix_L(self):
        """
        构造高程异常值向量
        :return: None
        """
        L = []
        for item in self.__parameter_point:
            L.append(item[2])
        return L

    def __calc__(self):
        """
        计算 X = (BTB)-1(BTL)
        :return: numpy.ndarray
        """
        b = self.__get_matrix_B()
        l = self.__get_matrix_L()
        B = numpy.array(b, dtype=numpy.float).reshape(self.number, 6)  # 10 * 6
        BT = B.transpose()  # 6 * 10
        BTB = numpy.matmul(BT, B)  # 6 * 6
        L = numpy.array(l, dtype=numpy.float).reshape(self.number, 1)  # 10 * 1
        BTL = numpy.matmul(BT, L)  # 6 * 1
        return numpy.matmul(pinv(BTB), BTL)

    @staticmethod
    def __calc_single_point_height_fitting(X, point):
        """
        计算单个点的高程异常值
        :param X: 参数列表
        :param point: 单个检查点
        :return: numpy.ndarray
        """
        check = [1, point[0], point[1], math.pow(point[0], 2), point[0] * point[1], math.pow(point[1], 2)]
        pt = numpy.array(check).reshape(1, 6)
        return numpy.matmul(pt, X).tolist()[0][0]

    # 得到正常高
    @staticmethod
    def __calc_get_normal_height(gps_hf, hf):
        return gps_hf - hf

    # 计算所有的高程异常值
    def CalcAllPointHf(self):
        """
        计算所有检查点的高程异常
        ：:rtype list<float>
        """
        # 得到 B 矩阵
        self.__get_matrix_B()
        # 得到 L 矩阵
        self.__get_matrix_L()

        # 计算 X = (BTB)-1(BTL)
        X = self.__calc__() # 6 * 1

        # 计算所有检查点的高程异常值
        exception = [Polynomial.__calc_single_point_height_fitting(X, item) for item in self.__check_point]
        return exception

    def CalcResidual(self,hf):
        """
        计算残差
        :param hf:所有检查点的高程异常差值
        :rtype list<float>
        """
        residual = []
        i = 0
        for item in self.__check_point:
            if len(item) > 3:
                residual.append(item[4] - hf[i])
                i = i + 1
            else:
                residual.append(item[2] - hf[i])
                i = i + 1
        return residual


if __name__ == '__main__':
    numpy.set_printoptions(suppress=True)
    src = DataProcessingAnalysis.DataProcessing('../../Data/gps_data_2.txt')
    basicData = src.Data
    p = Polynomial(basicData[0], 10)
    e = p.CalcAllPointHf()
    print(e)
