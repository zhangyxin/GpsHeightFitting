# -*- coding:utf-8 -*-

import os
import xlwt


class DataExport(object):
    """
    将处理后的数据进行导出
    """
    @staticmethod
    def export_to_txt(file_name, head, data):
        file_path = os.getcwd() + "\\" + "export"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        os.chdir(file_path)
        with open(file_name, "w+") as fp:
            # 写head
            for item in head:
                fp.write(item + '\t\t')
            fp.write('\r\n')
            for i in range(0, len(data)):
                for item in data[i]:
                    fp.write(item + '\t\t')
                fp.write('\r\n')
        return True

    @staticmethod
    def export_to_excel(file_name, sheet_name, head, data):
        file_path = os.getcwd() + "\\" + "export"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        os.chdir(file_path)\
        # 创建一个工作簿
        work_book = xlwt.Workbook()
        # 为工作簿添加表
        work_sheet = work_book.add_sheet(sheet_name)
        # 向表中添加数据
        # 1.写入表头
        for i in range(0, len(head)):
            work_sheet.write(0, i, label=head[i])
        # 2.写入数据
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                work_sheet.write(i + 1, j, label=data[i][j])
        work_book.save(file_name)
        return True

