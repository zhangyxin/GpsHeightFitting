# coding:utf-8

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 数据
# 平面拟合
a = [0.0086, 0.0138, 0.0037, -0.0036, 0.0006, 0.0084, -0.0143]
b = [0.0098, 0.0274, 0.0045, 0.0071, -0.0046, 0.0216, -0.0245]
c = [0.0101, 0.0214, 0.0012, -0.0057, -0.0013, 0.0126, -0.0211]
d = [0.0019, 0.0019, 0.0047, -0.001, 0.0014, 0.0018, 0]


def draw():
    plt.plot(a, label="平面拟合")
    plt.plot(b, label="双线性多项式内插")
    plt.plot(c, label="多项式曲面拟合")
    plt.plot(d, label="多面函数拟合")
    plt.legend(loc="lower left")
    plt.show()


if __name__ == '__main__':
    draw()