# -*- coding:utf-8 -*-

import math
import numpy


class Accuracy(object):
    """
    精度评定
    根据参与拟合计算已知点的高程异常ξi与拟合值ξ'i，用vi = ξ'i － ξi
    求拟合残差vi，按式(1) 计算GPS 高程拟合计算的内符合精度μ
    """
    def __init__(self):
        pass

    @staticmethod
    def evaluation_u1(residual, N, T=6):
        """
        :param residual: 已知点的高程异常 残差
        :param N: 参与计算的点个数
        :param T: 必要观测数
        :return: float
        """
        r = residual
        vi = numpy.array(r)
        vt = vi.transpose()
        return math.sqrt(math.fabs(numpy.matmul(vt, vi))/(N - T))

    @staticmethod
    def evaluation_u2(residual, num_of_check_point):
        """
        精度评定:外符合精度
        :param residual: 检核点残差
        :param num_of_check_point: 检核点的个数
        :return: float
        """
        r = residual
        v = numpy.array(r)
        vt = v.transpose()
        return math.sqrt(math.fabs(numpy.matmul(vt, v)) / num_of_check_point)

    @staticmethod
    def evaluation_fc(residual: list):
        """
        计算方差
        :param residual: 残差
        :return: float
        """
        arr = numpy.array(residual)
        return numpy.var(arr)

