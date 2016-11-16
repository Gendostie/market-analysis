#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from QT.test1 import Ui_Dialog


class ManagerTest(Ui_Dialog):
    # def setup_manager(self):
    #     self.buttonBox.accepted.connect(self.get_value)

    def get_values(self):
        return self.lineEdit.text()
