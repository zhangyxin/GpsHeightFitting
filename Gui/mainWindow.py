# -*- coding:utf-8 -*-
import copy
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QBrush
from PyQt5.QtCore import Qt
from Gui import MessageBox
from Gui.GpsDataView import GpsDataView
from Plot.DataView import DataView
from Src.Style import StyleSheet
from Src.DataProcess.DataProcessingAnalysis import *
from Src.Algorithm.polynomial_line import PolynomialLine
from Src.Algorithm.polynomial import Polynomial
from Src.Algorithm.AccuracySubStance import AccuracyStance
from Src.DataProcess.DataExport import DataExport
from Src.Algorithm.SurfaceFitting import PlaneFit
from pipe import argument


class Gps(QMainWindow):
    """
    :keyword mainWindow UI
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__gui_set()
        self.__toolbar_set()
        # 设置样式
        self.__style_set()
        # 保存一份原始数据引用
        self.basicData = None
        self.labels = None
        # 计算结果 高程异常值残差 tuple
        self.hf_set = []

    def __gui_set(self):
        """
        :keyword 设置主界面
        :return: None
        """
        # 设置可拖放
        self.setAcceptDrops(True)
        # 设置图标
        self.setWindowIcon(QIcon(r"./Img/ico.png"))
        # 设置标题
        self.setWindowTitle('Gps')
        # 窗口的尺寸
        self.setMinimumSize(840, 684)
        # 文件菜单
        self.file = self.menuBar().addMenu('文件')
        self.plot = self.menuBar().addMenu('原始散点分布图')
        self.surface = self.menuBar().addMenu('平面拟合法')
        self.qua_surface_fitting = self.menuBar().addMenu('二次曲面拟合法')
        self.bili_polynomial_inter = self.menuBar().addMenu('双线性多项式内插')
        self.polyhedral = self.menuBar().addMenu('多面函数法拟合')
        self.export = self.menuBar().addMenu('结果导出')
        self.about = self.menuBar().addMenu('关于')
        # MDI Widget
        self.mdi_widget = QMdiArea()
        self.setCentralWidget(self.mdi_widget)
        self.mdi_widget.setBackground(QBrush(QPixmap(r"./Img/mainViewBrush.jpg").scaled(self.width(), self.height())))
        # 添加动作
        self.import_data = self.file.addAction('导入数据')
        self.exit_app = self.file.addAction('退出')

        self.point = self.plot.addAction('散点图')

        self.surface_action = self.surface.addAction('计算高程异常')

        self.qua_hf = self.qua_surface_fitting.addAction('计算高程异常')
        self.qua_plot_scatter = self.qua_surface_fitting.addAction('plot散点图')
        self.qua_plot_zx = self.qua_surface_fitting.addAction('Hf折线图')
        # 设置不可用
        self.qua_hf.setEnabled(False)
        self.qua_plot_scatter.setEnabled(False)
        self.qua_plot_zx.setEnabled(False)

        self.bili_hf = self.bili_polynomial_inter.addAction('计算高程异常')
        self.bili_plot_scatter = self.bili_polynomial_inter.addAction('plot散点图')
        self.bili_plot_zx = self.bili_polynomial_inter.addAction('Hf折线图')

        # 设置不可用
        self.bili_hf.setEnabled(False)
        self.bili_plot_scatter.setEnabled(False)
        self.bili_plot_zx.setEnabled(False)

        self.polyhedral_action = self.polyhedral.addAction('计算高程异常')

        self.export_txt = self.export.addAction('导出到TXT')
        self.export_excel = self.export.addAction('导出到EXCEL')

        self.about_soft = self.about.addAction(QIcon('./Img/about.ico'), '关于本软件')

        # 关联槽函数
        self.import_data.triggered.connect(self.on_open_clicked)
        self.exit_app.triggered.connect(self.on_exit_app_clicked)
        self.point.triggered.connect(self.on_main_scatter)
        self.about_soft.triggered.connect(Gps.on_about_clicked)
        self.surface_action.triggered.connect(self.on_surface_clicked)
        self.qua_hf.triggered.connect(self.on_qua_surface_fitting_clicked)
        self.bili_hf.triggered.connect(self.on_bili_polynomial_inter_clicked)
        self.polyhedral_action.triggered.connect(self.on_polyhedral_clicked)
        self.export_txt.triggered.connect(self.on_export_txt_data)
        self.export_excel.triggered.connect(self.on_export_excel_data)
        self.qua_plot_scatter.triggered.connect(self.on_qua_scatter)
        self.bili_plot_scatter.triggered.connect(self.on_bili_scatter)

        self.qua_plot_zx.triggered.connect(self.on_qua_zx)
        self.bili_plot_zx.triggered.connect(self.on_bili_zx)

    # 设置工具栏
    def __toolbar_set(self):
        self.tooBar = QToolBar(self)
        self.tooBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.addToolBar(Qt.TopToolBarArea, self.tooBar)
        self.tooBar.addAction(QIcon('./Img/import_tool.ico'), '导入数据', self.on_open_clicked)
        self.tooBar.addAction(QIcon('./Img/scatter.ico'), '原始散点分布图', self.on_main_scatter)
        self.tooBar.addAction(QIcon('./Img/qua_s_f.ico'), '二次曲面拟合法', self.on_qua_surface_fitting_clicked)
        self.tooBar.addAction(QIcon('./Img/bili.ico'), '双线性多项式内插', self.on_bili_polynomial_inter_clicked)
        self.tooBar.addAction(QIcon('./Img/plot.ico'), '结果导出', self.on_export_txt_data)
        self.tooBar.addAction(QIcon('./Img/about.ico'), '关于', self.on_about_clicked)

    # 加载样式
    def __style_set(self):
        StyleSheet.StyleSheet.load("./resource/Style.qss", self)

    # 重写关闭事件
    # noinspection PyArgumentList
    def closeEvent(self, *args, **kwargs):
        button = QMessageBox.information(self, "退出", "确认退出？", QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            args[0].accept()
        else:
            args[0].ignore()

    def dragEnterEvent(self, *args, **kwargs):
        ev = args[0]
        if ev.mimeData().hasText():
            ev.acceptProposedAction()

    def dropEvent(self, *args, **kwargs):
        """
        重写拖放事件
        :param args: args[0] QDropEvent
        :param kwargs:
        :return:
        """
        ev = args[0]
        if ev.mimeData().hasText():
            name = ev.mimeData().text().split('///')[-1]
            self.on_open_clicked(file=name)

    # ---------------------------------------------------------------------------------------------------------
    # 槽函数
    # ---------------------------------------------------------------------------------------------------------
    def on_open_clicked(self, file=''):
        """
        打开文件
        :return: None
        """
        # 导入数据文件
        if not file:
            file_dlg = QFileDialog()
            file, file_type = file_dlg.getOpenFileName(parent=self, caption="导入数据", directory="./", filter="Text files (*.txt)", initialFilter=None, options=QFileDialog.ReadOnly)

        if file != '':
            # 构造数据解析对象
            data_obj = DataProcessing(file)
            self.basicData, self.labels = data_obj.Data
            if self.basicData is None:
                MessageBox.MessageOpenBox.show('打开文件错误', "请打开正确的数据文件")
                return
            MessageBox.MessageOpenBox.show('打开', '导入数据成功')
            # 设置数据处理可用
            self.qua_hf.setEnabled(True)
            self.bili_hf.setEnabled(True)

    def on_exit_app_clicked(self):
        """
        exit app
        """
        self.close()

    @staticmethod
    def on_about_clicked():
        """
        :keyword 关于
        """
        MessageBox.About.show()

    def on_surface_clicked(self):
        """
        平面拟合法
        :return:
        """
        if self.basicData is None:
            return
        pc = argument.Argu.read('PLANE/PC')
        model = self.__show('平面拟合法')
        # 计算检查点高程异常值
        p = PlaneFit(self.basicData,pc)
        e = p.CalcAllPointHf()
        # 保存 高程异常残差值
        self.hf_set.append(AccuracyStance('PLANE', p.CalcResidual(hf=e)))
        # 数据插入到ui中
        data = []
        for i in range(0, pc):
            data.append('参与平差')
        data.extend(e)
        model.appendColumnLast(headData=('拟合后高程异常', len(self.labels)), Data=data)

    def on_qua_surface_fitting_clicked(self):
        """
        二次曲面拟合法槽函数
        :return: None
        """
        if self.basicData is None:
            return
        pc = argument.Argu.QUASPC
        model = self.__show('二次曲面拟合法')
        # 计算检查点高程异常值
        p = Polynomial(self.basicData, pc)
        e = p.CalcAllPointHf()
        # 保存 高程异常残差值
        self.hf_set.append(AccuracyStance('QUASF', p.CalcResidual(hf=e)))
        # 数据插入到ui中
        data = []
        for i in range(0, pc):
            data.append('参与平差')
        data.extend(e)
        model.appendColumnLast(headData=('拟合后高程异常', len(self.labels)), Data=data)

    def on_bili_polynomial_inter_clicked(self):
        """
        双线性多项式内插
        :return: None
        """
        if self.basicData is None:
            return
        pc = argument.Argu.BILIPC
        model = self.__show('双线性多项式内插')
        # 计算检查点高程异常值
        p = PolynomialLine(self.basicData, pc)
        e = p.CalcAllPointHf()
        self.hf_set.append(AccuracyStance('BILI', p.CalcResidual(e)))
        # 数据插入到ui中
        data = []
        for i in range(0, pc):
            data.append('参与平差')
        data.extend(e)
        model.appendColumnLast(headData=('拟合后高程异常', len(self.labels)), Data=data)

    def on_polyhedral_clicked(self):
        """
        多面函数拟合
        :return:
        """
        if self.basicData is None:
            return
        from Src.Algorithm.PolyhedralFunctions import Polyhedral
        pc = argument.Argu.read('POLY/PC')
        model = self.__show('多面函数拟合')
        # 计算检查点高程异常值
        p = Polyhedral(self.basicData, pc)
        e = p.CalcAllPointHf()
        self.hf_set.append(AccuracyStance('POLY', p.CalcResidual(e)))
        # 数据插入到ui中
        data = []
        for i in range(0, pc):
            data.append('参与平差')
        data.extend(e)
        model.appendColumnLast(headData=('拟合后高程异常', len(self.labels)), Data=data)


    def on_qua_scatter(self):
        """
        :keyword 二次曲面拟合散点
        :return: None
        """
        DataView.scatters(self.basicData, argument.Argu.QUASPC)

    def on_bili_scatter(self):
        """
        :keyword 双线性多项式内插 散点
        :return:None
        """
        DataView.scatters(self.basicData, argument.Argu.BILIPC)

    def on_qua_zx(self):
        """
        :keyword 二次曲面拟合 折线图
        :return: None
        """
        for it in self.hf_set:
            if it.func_name == 'QUASF':
                DataView.zx(it.residual, 'plot-zx')

    def on_bili_zx(self):
        """
        多项式曲面拟合 折线图
        :return: None
        """
        for it in self.hf_set:
            if it.func_name == 'BILI':
                DataView.zx(it.residual, 'plot-zx')

    def __show(self, title):
        """
        创建视图
        :param title: 视图标题
        :return: 视图模型
        """
        handle = GpsDataView(title=title)
        sub_widget = QMdiSubWindow(None, Qt.Widget)
        sub_widget.setWidget(handle)
        self.mdi_widget.addSubWindow(sub_widget, Qt.Widget)
        sub_widget.resize(960, 640)
        sub_widget.show()
        handle.setWhatsThis(title)

        # 模型对象实例化
        gps_model = handle.GpsModel
        gps_model.insertHeadColumn(self.labels)
        # 将数据插入到模型中去
        if self.basicData is not None:
            data = copy.deepcopy(self.basicData)
            for item in data:
                gps_model.insertSingleRow(item)

        self.bili_plot_scatter.setEnabled(True)
        self.bili_plot_zx.setEnabled(True)
        self.qua_plot_scatter.setEnabled(True)
        self.qua_plot_zx.setEnabled(True)

        return gps_model

    def on_main_scatter(self):
        """
        画数据的原始散点图
        :return:
        """
        if self.basicData is not None:
            scatter = []
            for it in self.basicData:
                x = [it[0], it[1]]
                scatter.append(x)
            sc = DataView(scatter)
            sc.draw_scatter()

    def on_export_txt_data(self):
        """
        导出计算结果 txt
        :return:
        """
        if self.basicData is None or len(self.hf_set) == 0:
            return
        # 获得当前 MDI->SubWidget->Widget->model 窗口句柄
        current_model = self.mdi_widget.activeSubWindow().widget().GpsModel
        data = current_model.ergodic()
        if DataExport.export_to_txt('out4.txt', head=current_model.HeadData, data=data):
            MessageBox.MessageOpenBox.success('导出成功', "数据导出成功！")

    def on_export_excel_data(self):
        """
        导出计算结果 EXCEL
        :return: None
        """
        if self.basicData is None or len(self.hf_set) == 0:
            return
        title = self.mdi_widget.activeSubWindow().windowTitle()
        # 获得当前 MDI->SubWidget->Widget->model 窗口句柄
        current_model = self.mdi_widget.activeSubWindow().widget().GpsModel
        data = current_model.ergodic()
        if DataExport.export_to_excel(title + '.xls', sheet_name='data', head=current_model.HeadData, data=data):
            MessageBox.MessageOpenBox.success('导出成功', "数据导出成功！")
