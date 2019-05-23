# -*- coding:utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class DataView(object):
    """
    对传入的数据进行plot绘图
    """
    def __init__(self, data : list):
        self.data = data

    def show(self, x_lable= None, y_lable= None):
        array = np.array(self.data)
        plt.plot(array)
        plt.xlabel(x_lable)
        plt.ylabel(y_lable)
        plt.show()

    def draw_scatter(self):
        x = []
        y = []
        for item in self.data:
            x.append(item[0])
            y.append(item[1])
        plt.scatter(x, y)
        plt.show()

    @staticmethod
    def scatters(basicData, p_num):
        """
        散点图
        :param basicData: 原始数据
        :param p_num: 平差点的数量
        :return:
        """
        check = basicData[p_num:]
        calc = basicData[:p_num]
        x = []
        y = []
        for it in calc:
            x.append(it[0])
            y.append(it[1])
        cx = []
        cy = []
        for it in check:
            cx.append(it[0])
            cy.append(it[1])
        plt.scatter(x, y, marker='x', edgecolors='red', s=40, label=u"拟合点")
        plt.scatter(cx, cy, marker='o', edgecolors='green', s=40, label=u"检查点")
        plt.legend(loc='best')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xticks(rotation=45)

        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')  # 设置 上、右 两条边框不显示
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')  # 将下、左 两条边框分别设置为 x y 轴
        # ax.spines['bottom'].set_position(('data', 499500))  # 将两条坐标轴的交点进行绑定
        # ax.spines['left'].set_position(('data', 3566000))
        plt.show()

    @staticmethod
    def zx(hf_data, title):
        """
        折线图
        :param hf_data: 高程异常值
        :param title: 标题
        :return:
        """
        plt.plot(hf_data, label = 'height fitting')
        plt.title(label=title)
        plt.show()
