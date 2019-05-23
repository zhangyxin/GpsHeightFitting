# -*- coding:utf-8 -*-
from Src.DataProcess.DataProcessingAnalysis import *
from Src.Algorithm.AbstractHeightFitting import AbstractFitting
import numpy as np
from numpy.linalg import pinv


class PolynomialLine(AbstractFitting):
    """
    :keyword 双线性多项式内插
    :keyword z = a0 + a1x + a2y + a3xy
    """
    def __init__(self, basic_data, number_of_param):
        if basic_data is None:
            raise Exception('The imported data is NoneType!')
        self.__param_point = basic_data[:number_of_param]
        self.__check_point = basic_data[number_of_param:]
        # 系数矩阵
        self.matrix_B = []
        # 高程异常值向量
        self.matrix_Z = []
        self.number = number_of_param

    def __str__(self):
        return "双线性多项式内插"

    def __calc_matrix_b(self):
        """
        :keyword 计算系数矩阵
        """
        for item in self.__param_point:
            self.matrix_B.append([1, item[0], item[1], item[0] * item[1]])

    def __calc_z(self):
        """
        :keyword 计算出 z
        """
        for item in self.__param_point:
            if len(item) > 3:
                self.matrix_Z.append(item[4])
            else:
                self.matrix_Z.append(item[2])

    def __calc(self):
        """
        :keyword 根据间接平差 计算 (BTB)-1 * (BTL)
        :return 返回 numpy.ndarray 计算出的参数列表
        """
        B = np.array(self.matrix_B).reshape(self.number, 4)
        BT = B.transpose()
        BTB = np.matmul(BT, B)
        for it in BTB:
            print(it)
        Z = np.array(self.matrix_Z).reshape(self.number, 1)  # 10 * 1
        BTZ = np.matmul(BT, Z)  # 6 * 1
        return np.matmul(pinv(BTB), BTZ)

    @staticmethod
    def __calc_all_hf(x, check_point):
        hf_t = []
        for item in check_point:
            check = [1, item[0], item[1], item[0] * item[1]]
            c = np.array(check).reshape(1, 4)
            hf_t.append(np.matmul(c, x)[0][0])
        return hf_t

    def CalcAllPointHf(self):
        """
        :keyword    计算所有检查点的高程异常
        :return     list
        """
        self.__calc_matrix_b()
        self.__calc_z()
        x = self.__calc()
        return PolynomialLine.__calc_all_hf(x, self.__check_point)

    def CalcResidual(self, hf):
        """
        :keyword 计算检查点的高程异常残差
        :param hf 计算出的拟合高程异常值
        :type hf list
        :return list 所有检查点的高程异常残差值
        """
        if len(hf) != 0:
            residual = []
            for i in range(0, len(self.__check_point)):
                if len(self.__check_point[i]) > 3:
                    residual.append(self.__check_point[i][4] - hf[i])
                else:
                    residual.append(self.__check_point[i][2] - hf[i])
            return residual
        else:
            return None


if __name__ == '__main__':
    data_obj = DataProcessing("../../Data/gps_data_1.txt")
    basicData, headLables = data_obj.Data
    p = PolynomialLine(basicData, 10)
    h = p.CalcAllPointHf()
    print(h)
    print(p.CalcResidual(h))


