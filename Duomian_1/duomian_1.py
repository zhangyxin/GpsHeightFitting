# coding:utf-8

from Src.Algorithm.PolyhedralFunctions import *
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def test(gm_t):
    # 解决多面函数法中 平滑因子从小到大变化过程中残差的变化
    s = DataProcessing('../Data/gps_data_1.txt')
    basic_data = s.Data
    pobj = Polyhedral(basic_data[0], 10)
    pobj.gm = gm_t
    residual = pobj.CalcAllPointHf()
    return pobj.CalcResidual(residual)


def write(data_list):
    with open('../export/gm.txt', 'w') as f:
        for it in data_list:
            f.write(str(it) + "\t")
        f.write("\r\n")


if __name__ == '__main__':
    for i in range(1000, 10000, 1000):
        # print(test(i))
        plt.plot(test(i), label=str(i))
    plt.legend(loc='upper left')
    plt.title("随平滑因子增大残差的变化图")
    plt.xlabel('点号')
    plt.ylabel('残差\cm')
    plt.show()

