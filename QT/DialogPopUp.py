# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogPopUp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(301, 177)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 140, 281, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_minInvest = QtGui.QLabel(Dialog)
        self.label_minInvest.setGeometry(QtCore.QRect(10, 12, 160, 20))
        self.label_minInvest.setMaximumSize(QtCore.QSize(160, 20))
        self.label_minInvest.setObjectName(_fromUtf8("label_minInvest"))
        self.doubleSpinBox_minInvest = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_minInvest.setGeometry(QtCore.QRect(160, 10, 130, 25))
        self.doubleSpinBox_minInvest.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_minInvest.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_minInvest.setMaximum(999999999.99)
        self.doubleSpinBox_minInvest.setSingleStep(100.0)
        self.doubleSpinBox_minInvest.setProperty("value", 1000.0)
        self.doubleSpinBox_minInvest.setObjectName(_fromUtf8("doubleSpinBox_minInvest"))
        self.label_maxInvest = QtGui.QLabel(Dialog)
        self.label_maxInvest.setGeometry(QtCore.QRect(10, 60, 160, 20))
        self.label_maxInvest.setMaximumSize(QtCore.QSize(160, 20))
        self.label_maxInvest.setObjectName(_fromUtf8("label_maxInvest"))
        self.doubleSpinBox_maxInvest = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_maxInvest.setGeometry(QtCore.QRect(160, 58, 130, 25))
        self.doubleSpinBox_maxInvest.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_maxInvest.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_maxInvest.setMaximum(999999999.99)
        self.doubleSpinBox_maxInvest.setSingleStep(100.0)
        self.doubleSpinBox_maxInvest.setProperty("value", 2000.0)
        self.doubleSpinBox_maxInvest.setObjectName(_fromUtf8("doubleSpinBox_maxInvest"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Parameters Specifics Simulation", None))
        self.label_minInvest.setText(_translate("Dialog", "Minimum Investment", None))
        self.doubleSpinBox_minInvest.setSuffix(_translate("Dialog", " $", None))
        self.label_maxInvest.setText(_translate("Dialog", "Maximum Investment", None))
        self.doubleSpinBox_maxInvest.setSuffix(_translate("Dialog", " $", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

