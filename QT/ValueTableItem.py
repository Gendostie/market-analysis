from PyQt4 import QtGui
from QT.Order_Manager import singleton


# TODO : Add comments
class value_tableitem(QtGui.QTableWidgetItem):
    def __lt__(self, other):
        try:
            if self.text() == "":
                value = float("-inf") if singleton.get_order(singleton()) else float("inf")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value < other

    def __le__(self, other):
        try:
            if self.text() == "":
                value = float("-inf") if singleton.get_order(singleton()) else float("inf")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value <= other

    def __eq__(self, other):
        try:
            if self.text() == "":
                value = float("nan")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value == other

    def __ne__(self, other):
        try:
            if self.text() == "":
                value = float("nan")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value != other

    def __gt__(self, other):
        try:
            if self.text() == "":
                value = float("-inf") if singleton.get_order(singleton()) else float("inf")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value > other

    def __ge__(self, other):
        try:
            if self.text() == "":
                value = float("-inf") if singleton.get_order(singleton()) else float("inf")
            else:
                value = float(self.text())
        except ValueError:
            value = self.text()
        return value >= other
