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
        Dialog.resize(435, 253)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 210, 411, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_minInvest = QtGui.QLabel(Dialog)
        self.label_minInvest.setGeometry(QtCore.QRect(10, 12, 160, 20))
        self.label_minInvest.setObjectName(_fromUtf8("label_minInvest"))
        self.doubleSpinBox_minInvest = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_minInvest.setGeometry(QtCore.QRect(170, 10, 130, 25))
        self.doubleSpinBox_minInvest.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_minInvest.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_minInvest.setMaximum(999999999.99)
        self.doubleSpinBox_minInvest.setProperty("value", 0.0)
        self.doubleSpinBox_minInvest.setObjectName(_fromUtf8("doubleSpinBox_minInvest"))
        self.label_maxInvest = QtGui.QLabel(Dialog)
        self.label_maxInvest.setGeometry(QtCore.QRect(10, 60, 160, 20))
        self.label_maxInvest.setObjectName(_fromUtf8("label_maxInvest"))
        self.doubleSpinBox_maxInvest = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_maxInvest.setGeometry(QtCore.QRect(170, 58, 130, 25))
        self.doubleSpinBox_maxInvest.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_maxInvest.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_maxInvest.setMaximum(999999999.99)
        self.doubleSpinBox_maxInvest.setProperty("value", 0.0)
        self.doubleSpinBox_maxInvest.setObjectName(_fromUtf8("doubleSpinBox_maxInvest"))
        self.cb_typeInvest = QtGui.QComboBox(Dialog)
        self.cb_typeInvest.setGeometry(QtCore.QRect(139, 108, 285, 25))
        self.cb_typeInvest.setObjectName(_fromUtf8("cb_typeInvest"))
        self.cb_typeInvest.addItem(_fromUtf8(""))
        self.cb_typeInvest.addItem(_fromUtf8(""))
        self.label_meanInvest = QtGui.QLabel(Dialog)
        self.label_meanInvest.setGeometry(QtCore.QRect(10, 110, 131, 20))
        self.label_meanInvest.setObjectName(_fromUtf8("label_meanInvest"))
        self.label_nbMaxCieInvest = QtGui.QLabel(Dialog)
        self.label_nbMaxCieInvest.setGeometry(QtCore.QRect(10, 158, 210, 20))
        self.label_nbMaxCieInvest.setObjectName(_fromUtf8("label_nbMaxCieInvest"))
        self.doubleSpinBox_nbMaxCieInvest = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox_nbMaxCieInvest.setGeometry(QtCore.QRect(220, 156, 81, 25))
        self.doubleSpinBox_nbMaxCieInvest.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_nbMaxCieInvest.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_nbMaxCieInvest.setSuffix(_fromUtf8(""))
        self.doubleSpinBox_nbMaxCieInvest.setDecimals(0)
        self.doubleSpinBox_nbMaxCieInvest.setMaximum(1000000.0)
        self.doubleSpinBox_nbMaxCieInvest.setProperty("value", 0.0)
        self.doubleSpinBox_nbMaxCieInvest.setObjectName(_fromUtf8("doubleSpinBox_nbMaxCieInvest"))

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
        self.cb_typeInvest.setItemText(0, _translate("Dialog", "Invest in as much company possible", None))
        self.cb_typeInvest.setItemText(1, _translate("Dialog", "Inverst in as much money possible", None))
        self.label_meanInvest.setText(_translate("Dialog", "Mean Investment", None))
        self.label_nbMaxCieInvest.setText(_translate("Dialog", "Nb max companies to invest", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

