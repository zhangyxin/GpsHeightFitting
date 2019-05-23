# coding: utf-8
from abc import ABC,abstractmethod

class AbstractFitting(ABC):

    @abstractmethod
    def CalcAllPointHf(cls):
        raise NotImplementedError

    @abstractmethod
    def CalcResidual(self,hf):
        raise NotImplementedError