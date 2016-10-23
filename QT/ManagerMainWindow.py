#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow, _translate
from Manager_DB import ManagerCompany
import HelperFunctionQt


class ManagerMainWindow(Ui_MainWindow):
    def setup_size_fixed(self):
        """
        Put min and max size of widget like main window for size fixed in setup Ui_MainWindow
        :return: None
        """
        # fixed size main window
        MainWindow.setMaximumSize(MainWindow.size())
        MainWindow.setMinimumSize(MainWindow.size())
        # adjust column of table widget
        self.tableWidget_stockScreener.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeToContents)

    def create_data_table_stock_screener(self):
        """
        Create data in table widget stock screener with data SQL
        :return: None
        """
        list_column_table = ['company_name', 'symbol', 'stock_value', 'income', 'gross_margin',
                             'dividends', 'market_capitaisation', 'finantical_index', 'index_end', 'earning',
                             'book_value', 'sales_value', 'cash_flow']
        list_company = ManagerCompany.get_historic_value_all_company()

        if self.tableWidget_stockScreener.rowCount() < len(list_company):
            self.tableWidget_stockScreener.setRowCount(len(list_company))

        sorting_enable = self.tableWidget_stockScreener.isSortingEnabled()
        self.tableWidget_stockScreener.setSortingEnabled(False)
        for idx_row, company in enumerate(list_company):
            row_items = []
            for key in company.keys():
                try:
                    idx_column = list_column_table.index(key)
                    assert (idx_column > 0 or idx_column < self.tableWidget_stockScreener.rowCount()), \
                        'Problem index of column when insert new row'
                    # create new row
                    cell = QtGui.QTableWidgetItem()
                    # we don't want user can change value of cell in table
                    cell.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    value = company.get(key) if company.get(key) is not None else ""
                    cell.setText(_translate("MainWindow", value, None))
                    self.tableWidget_stockScreener.setItem(idx_row, idx_column, cell)
                except ValueError:
                    continue  # if column no exists in table stock screener, we continue
            # create checkbox in last cell of row
            widget_cb = QtGui.QWidget()
            h_box_layout_cb = QtGui.QHBoxLayout()
            cb = QtGui.QCheckBox()
            h_box_layout_cb.setMargin(1)
            h_box_layout_cb.setAlignment(QtCore.Qt.AlignCenter)
            h_box_layout_cb.addWidget(cb)
            widget_cb.setLayout(h_box_layout_cb)
            # we suppose checkbox is always in end of row
            self.tableWidget_stockScreener.setCellWidget(idx_row,
                                                         self.tableWidget_stockScreener.columnCount() - 1,
                                                         widget_cb)
        self.tableWidget_stockScreener.setSortingEnabled(sorting_enable)

    def create_connexion_signal_slot(self):
        self.btn_stockScreener_addPortfolio.clicked\
            .connect(sort_column_checkbox_table_widget_stock_screener)


def sort_column_checkbox_table_widget_stock_screener():
    table_widget = ui.tableWidget_stockScreener
    # sort_order = 0 => ascending ; Qt::Unchecked = 0  Qt::Checked = 2  Qt::PartiallyChecked = 1
    sort_order = table_widget.horizontalHeader().sortIndicatorOrder()
    sort_indicator = table_widget.horizontalHeader().sortIndicatorSection()
    nb_column = table_widget.columnCount()
    # put value of same scale of checkbox state
    sort_order = 0 if sort_order == 1 or sort_indicator != nb_column - 1 else 2
    if table_widget.rowCount() > 0:
        list_row_remove = []
        for idx in range(table_widget.rowCount()):
            # get checkbox widget
            cb = table_widget.cellWidget(idx, nb_column - 1).layout().itemAt(0).widget()
            # ascending = Unchecked to Checked ; descending = Checked to Unchecked
            if cb.checkState() != sort_order:
                row = HelperFunctionQt.take_row_table_widget(table_widget, idx)
                HelperFunctionQt.set_row_table_widget(table_widget, row)
                list_row_remove.append(idx)
        list_row_remove.reverse()
        for idx in list_row_remove:
            table_widget.removeRow(idx)
    sort_order = 1 if sort_order == 2 else 0  # put value of sort state
    table_widget.horizontalHeader().setSortIndicator(nb_column - 1, sort_order)  # set indicator column sort


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = ManagerMainWindow()
    ui.setupUi(MainWindow)

    ui.setup_size_fixed()
    ui.create_data_table_stock_screener()
    ui.create_connexion_signal_slot()

    MainWindow.show()
    sys.exit(app.exec_())
