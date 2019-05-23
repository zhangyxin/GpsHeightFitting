# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap,QIcon


class About(object):

    @staticmethod
    def show():
        messageBox = QMessageBox()
        messageBox.setWindowTitle('About')
        messageBox.setWindowIcon(QIcon('./Img/about.ico'))
        messageBox.setIconPixmap(QPixmap('./Img/ico.png').scaled(100,100))
        messageBox.setText("\n\nGps Height Fitting\n version:1.0")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.show()
        messageBox.exec_()

class MessageOpenBox(object):

    @staticmethod
    def show(title, text):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(title)
        messageBox.setText(text)
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.setWindowIcon(QIcon('./Img/importData.ico'))
        messageBox.setIconPixmap(QPixmap('./Img/importData.png').scaled(60,40))
        messageBox.show()
        messageBox.exec_()

    @staticmethod
    def success(title,text):
        messageBox = QMessageBox()
        messageBox.setWindowTitle(title)
        messageBox.setText(text)
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.setWindowIcon(QIcon('../Img/success.ico'))
        messageBox.setIconPixmap(QPixmap('../Img/success.ico').scaled(50, 50))
        messageBox.show()
        messageBox.exec_()
