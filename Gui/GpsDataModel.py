# -*- coding:utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class GpsDataModel(object):
    """
    :keyword Model QStandItemModel
    """
    def __init__(self):
        self.__stand_item_model = QStandardItemModel()

    @property
    def Model(self):
        return self.__stand_item_model

    @property
    def HeadData(self):
        return [str(self.__stand_item_model.headerData(i, Qt.Horizontal)) for i in range(0, self.__stand_item_model.columnCount())]

    # 插入单行
    def insertSingleRow(self,Data : tuple):
        item = []
        count = len(Data)
        for i in range(0,count):
            item.append(QStandardItem(str(Data[i])))
        self.__stand_item_model.appendRow(item)

    # 插入多行
    def insertMultiRows(self, DataList : list):
        for i in range(0, len(DataList)):
            self.insertSingleRow(DataList[i])

    def insertSingleColumn(self, headData, Data:tuple, column):
        """
        :keyword 插入单列
        :param HeadData : label Data : tuple column : to insert into column
        """
        list_stand_item = [QStandardItem(str(data)) for data in Data]
        self.__stand_item_model.insertColumn(4, list_stand_item)
        self.__stand_item_model.setHorizontalHeaderItem(column, QStandardItem(headData))

    # 插入多列
    def insertHeadColumn(self, headData:list):
        self.__stand_item_model.setHorizontalHeaderLabels(headData)

    def appendColumnLast(self,headData:tuple, Data):
        """
        在最后插入一列
        :param: headData: (label,Last_column_number) Data : iter
        """
        list_stand_item = [QStandardItem(str(item)) for item in Data]
        self.__stand_item_model.appendColumn(list_stand_item)
        self.__stand_item_model.setHorizontalHeaderItem(headData[1], QStandardItem(headData[0]))

    def ergodic(self):
        """
        遍历所有单元格并将数据导出到本地
        :return: tuple
        """
        # 获得行列数
        rows = self.__stand_item_model.rowCount()
        columns = self.__stand_item_model.columnCount()
        # 按行列获取单元格
        data = []
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                try:
                    row.append(self.__stand_item_model.item(i, j).text())
                except:
                    row.append('')
            data.append(row)
        return data

    def ergodic_column(self, column):
        data = []
        rows = self.__stand_item_model.rowCount()
        for i in range(0, rows):
            data.append(self.__stand_item_model.item(i, column).text())
        return data