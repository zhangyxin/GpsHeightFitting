# coding: utf-8


class AccuracyStance(object):
    """
    :keyword 实体类
    """
    def __init__(self, func_name, residual, *args, **kwargs):
        # 函数名
        self.func_name = func_name
        # 残差
        self.residual = residual
