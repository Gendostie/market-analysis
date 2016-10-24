#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from MainWindow import Ui_MainWindow, _translate
import ManagerCompany
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
        """
        Add connection between signal (ex:click button) and slot (action to do, ex: open dialog box)
        :return: None
        """
        # sort column checkbox of table stock screnner
        self.tableWidget_stockScreener.horizontalHeader().sectionClicked\
            .connect(Slots.sort_column_checkbox_table_widget_stock_screener)
        # checked or unchecked the checkbox of cell clicked
        self.tableWidget_stockScreener.cellClicked.connect(Slots.modify_checkbox_table_widget_stock_screener)
        # link slider and spin box of box layout to left
        for idx_h_layout in range(self.verticalLayout_left.count()):
            min_spin_box = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_left.itemAt(idx_h_layout),
                                                                  QtGui.QDoubleSpinBox)
            min_range_slider = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_left.itemAt(idx_h_layout),
                                                                     QtGui.QSlider)
            min_spin_box.valueChanged.connect(min_range_slider.setValue)
            min_range_slider.valueChanged.connect(min_spin_box.setValue)

            max_spin_box = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_left.itemAt(idx_h_layout),
                                                                  QtGui.QDoubleSpinBox, 1)

            max_range_slider = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_left.itemAt(idx_h_layout),
                                                                  QtGui.QSlider, 1)
            max_spin_box.valueChanged.connect(max_range_slider.setValue)
            max_range_slider.valueChanged.connect(max_spin_box.setValue)
        # link slider and spin box of box layout to right
        for idx_h_layout in range(self.verticalLayout_right.count()):
            min_spin_box = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_right.itemAt(idx_h_layout),
                                                                 QtGui.QDoubleSpinBox)
            min_range_slider = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_right.itemAt(idx_h_layout),
                                                                     QtGui.QSlider)
            min_spin_box.valueChanged.connect(min_range_slider.setValue)
            min_range_slider.valueChanged.connect(min_spin_box.setValue)

            max_spin_box = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_right.itemAt(idx_h_layout),
                                                                 QtGui.QDoubleSpinBox, 1)

            max_range_slider = HelperFunctionQt.get_widget_of_layout(self.verticalLayout_right.itemAt(idx_h_layout),
                                                                     QtGui.QSlider, 1)
            max_spin_box.valueChanged.connect(max_range_slider.setValue)
            max_range_slider.valueChanged.connect(max_spin_box.setValue)



class Slots:
    @staticmethod
    def modify_checkbox_table_widget_stock_screener(row, column):
        """
        Give possibility to user to click cell of checkbox fo check or uncheck case
        :param row: row cell clicked
        :type row: int
        :param column: column of celll clicked
        :type column: int
        :return: None
        """
        if column == ui.tableWidget_stockScreener.columnCount() - 1:
            # get checkbox widget
            cb = ui.tableWidget_stockScreener.cellWidget(row, column).layout().itemAt(0).widget()
            cb.setChecked(not cb.isChecked())

    @staticmethod
    def sort_column_checkbox_table_widget_stock_screener(column):
        """
        Sorted column with checkbox, ascending = Unchecked to Checked ; descending = Checked to Unchecked
        :param column: column of header cell clicked
        :type column: int
        :return: None
        """
        table_widget = ui.tableWidget_stockScreener
        if column == table_widget.columnCount() - 1:
            # sort_order = 0 => ascending ; Qt::Unchecked = 0  Qt::Checked = 2  Qt::PartiallyChecked = 1
            sort_order = table_widget.horizontalHeader().sortIndicatorOrder()
            # sort_indicator = table_widget.horizontalHeader().sortIndicatorSection()
            # put value of same scale of checkbox state
            sort_order = 2 if sort_order == 1 else sort_order
            if table_widget.rowCount() > 0:
                list_row_remove = []
                for idx in range(table_widget.rowCount()):
                    # get checkbox widget
                    cb = HelperFunctionQt.get_widget_of_layout(table_widget.cellWidget(idx, column).layout(),
                                                               QtGui.QCheckBox)
                    if cb.checkState() != sort_order:
                        row = HelperFunctionQt.take_row_table_widget(table_widget, idx)
                        HelperFunctionQt.set_row_table_widget(table_widget, row)
                        list_row_remove.append(idx)
                list_row_remove.reverse()
                for idx in list_row_remove:
                    table_widget.removeRow(idx)
            sort_order = 1 if sort_order == 2 else sort_order  # put value of sort state
            table_widget.horizontalHeader().setSortIndicator(column, sort_order)  # set indicator column sort


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
