# -*- coding:utf-8 -*-

import os.path

class StyleSheet(object):
    """
    为窗口加载样式
    """
    @staticmethod
    def load(qss,win):
        if not os.path.isfile(qss):
            return
        with open(qss, "r") as f:
            qs = f.readlines()
            style = ''.join(qs).strip('\n')
        win.setStyleSheet(style)