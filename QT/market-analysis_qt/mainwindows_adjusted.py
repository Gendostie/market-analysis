#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import mainwindow

from Manager_DB import ManagerCompany


class UiMainWindowAdjusted(mainwindow.Ui_MainWindow):
    @staticmethod
    def setup_size_fixed():
        """
        Put min and max size of windows to size fixed in setup Ui_MainWindow
        :return: None
        """
        MainWindow.setMaximumSize(MainWindow.size())
        MainWindow.setMinimumSize(MainWindow.size())

    def create_data_table_stock_screener(self):
        list_column_table = ['company_name', 'symbol', 'stock_value', 'income', 'gross_margin',
                            'dividends', 'market_capitaisation', 'finantical_index', 'index_end', 'earning',
                            'book_value', 'sales_value', 'cash_flow']
        list_company = ManagerCompany.get_historic_value_all_company()

        if self.tableWidget_stockScreener.rowCount() < len(list_company):
            self.tableWidget_stockScreener.setRowCount(len(list_company))

        SORTING_ENABLE = self.tableWidget_stockScreener.isSortingEnabled()
        self.tableWidget_stockScreener.setSortingEnabled(False)
        for idx_row, company in enumerate(list_company):
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
                    cell.setText(mainwindow._translate("MainWindow", value, None))
                    self.tableWidget_stockScreener.setItem(idx_row, idx_column, cell)
                except ValueError:
                    continue  # if column no exists in table stock screener, we continue
            # create checkbox in last cell of row
            widget_cd = QtGui.QWidget()
            h_box_layout_cb = QtGui.QHBoxLayout()
            cb = QtGui.QCheckBox()
            h_box_layout_cb.setMargin(1)
            h_box_layout_cb.setAlignment(QtCore.Qt.AlignCenter)
            h_box_layout_cb.addWidget(cb)
            widget_cd.setLayout(h_box_layout_cb)
            # we suppose checkbox is always in end of row
            self.tableWidget_stockScreener.setCellWidget(idx_row,
                                                         self.tableWidget_stockScreener.columnCount() - 1,
                                                         widget_cd)
        self.tableWidget_stockScreener.setSortingEnabled(SORTING_ENABLE)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = UiMainWindowAdjusted()
    ui.setupUi(MainWindow)

    ui.setup_size_fixed()
    ui.create_data_table_stock_screener()

    MainWindow.show()
    sys.exit(app.exec_())
