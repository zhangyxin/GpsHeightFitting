# coding: utf-8

from PyQt5.QtCore import QSettings


class Setting(object):
    """
    配置文件
    """
    def __init__(self):
        pass

    @staticmethod
    def read(key: str):
        setting = QSettings('argu.ini', QSettings.IniFormat)
        return int(setting.value(key))
