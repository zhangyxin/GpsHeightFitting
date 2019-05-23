# -*- coding:utf-8 -*-

from Gui.GpsDataModel import GpsDataModel
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView, QWidget, QMenuBar, QMenu
from PyQt5.QtGui import QIcon
from Gui import GpsDataModel
from Src.Style import StyleSheet


class GpsDataView(QWidget):
    """
    主界面显示数据视图
    """

    # noinspection PyArgumentList
    def __init__(self, title='数据处理'):
        super(GpsDataView, self).__init__()
        self.__main_view = QTableView(parent=self)
        self.__gps_model = None
        self.title = title
        self.__menuBar()
        self.__create()
        self.isAccuracy = False

    @property
    def GpsModel(self):
        return self.__gps_model

    @property
    def GpsView(self):
        return self.__main_view

    def __menuBar(self):
        """
        menubar
        :return:
        """
        self.__menu_bar = QMenuBar(parent=self)
        self.__menu_bar.addAction('残差计算', self.on_residual)
        self.__menu_bar.addAction('精度评定', self.on_accuracy)

    def __create(self):
        self.__gps_model = GpsDataModel.GpsDataModel()
        self.setWindowIcon(QIcon('./Img/data.ico'))
        self.setWindowTitle(self.title)
        self.__main_view.setModel(self.__gps_model.Model)
        # 设置表头与网格对齐
        self.__main_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置网格禁止被编辑
        self.__main_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置选择单元格的方式:选择一行
        self.__main_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 隐藏行号
        self.__main_view.verticalHeader().hide()
        # 设置样式
        StyleSheet.StyleSheet.load("./resource/DataViewStyle.qss", self.__main_view)
        # 设置位置
        self.__main_view.setGeometry(0, 23, self.width(), self.height())

    def resizeEvent(self, QResizeEvent):
        # 获得大小改变后的尺寸
        size = QResizeEvent.size()
        # 重置 view 的大小
        self.__main_view.resize(size)
        # 改变MenuBar大小
        self.__menu_bar.setGeometry(0, 0, self.width(), 23)

    def on_accuracy(self):
        """
        精度计算并导入model
        :return:
        """
        if self.isAccuracy:
           return
        from pipe import argument
        from Src.Algorithm.accuracy_evaluation import Accuracy
        try:
            data1 = self.__gps_model.ergodic_column(4)
            data2 = self.__gps_model.ergodic_column(5)
        except:
            data1 = self.__gps_model.ergodic_column(2)
            data2 = self.__gps_model.ergodic_column(3)

        T = 6
        N = 12

        if self.whatsThis() == '二次曲面拟合法':
            T, N = argument.Argu.QUANECE, argument.Argu.QUASPC
        elif self.whatsThis() == '双线性多项式内插':
            T, N = argument.Argu.BILINECE, argument.Argu.BILIPC
        elif self.whatsThis() == '平面拟合法':
            T, N = argument.Argu.read('PLANE/NECESSARY'), argument.Argu.read('PLANE/PC')
        elif self.whatsThis() == '多面函数拟合':
            T, N = argument.Argu.read('POLY/NECESSARY'), argument.Argu.read('PLANE/PC')
        else:
            T = 6
        # 残差
        residual = [(float(data1[i]) - float(data2[i])) for i in range(N, len(data2))]
        in_acc = Accuracy.evaluation_u1(residual, N, T)
        out_acc = Accuracy.evaluation_u2(residual, len(data2) - N)
        fc = Accuracy.evaluation_fc([it*100 for it in residual])
        self.__gps_model.insertSingleRow(('内符合精度:', in_acc, '外符合精度:', out_acc, "方差:", fc))

        self.isAccuracy = True

    def on_residual(self):
        """
        残差计算
        """
        if '残差' in self.__gps_model.HeadData:
            return
        column = self.__gps_model.Model.columnCount()
        row = self.__gps_model.Model.rowCount()
        if self.isAccuracy:
            row = row - 1
        last = [self.__gps_model.Model.item(i, column - 1).text() for i in range(0, row)]
        prev = [self.__gps_model.Model.item(i, column - 2).text() for i in range(0, row)]
        # 计算
        event = []
        for i in range(0, len(last)):
            try:
                event.append(float(prev[i]) - float(last[i]))
            except:
                event.append('参与计算')
        self.__gps_model.appendColumnLast(headData=('残差', column), Data=event)
