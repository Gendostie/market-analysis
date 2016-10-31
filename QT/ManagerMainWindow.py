#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from QT.MainWindow import Ui_MainWindow, _translate
import Manager_DB.ManagerCompany as ManagerCompany
import Manager_DB.ManagerPortfolio as ManagerPortfolio
import QT.HelperFunctionQt as HelperFunctionQt
import QT.ValueTableItem as ValueTableItem


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
        # TODO : Ne fonctionne pas sur mon ordinateur alors temporairement désactivé.
        # self.tableWidget_stockScreener.horizontalHeader().setSectionResizeMode(QtGui.QHeaderView.ResizeToContents)

        # TODO : Add comment
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_left)
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_right)

    def setup_manager(self):
        """
        Setup for widget already in MainWindow.ui to modify
        :return: None
        """
        self.comboBox_stockScreener_portfolio.lineEdit().setPlaceholderText("Choose your portfolio name.")
        self.add_portfolio_name_in_combobox('tabStockScreener', 'comboBox_stockScreener_portfolio')

    def create_data_table_stock_screener(self):
        """
        Create data in table widget stock screener with data SQL
        :return: None
        """
        list_column_table = ['company_name', 'symbol', 'close', 'revenue', 'gross_margin', 'net_income', 'dividends',
                             'EPS', 'BVPS', 'free_cash_flow_per_share']
        list_company = ManagerCompany.get_historic_value_all_company()

        if self.tableWidget_stockScreener.rowCount() < len(list_company):
            self.tableWidget_stockScreener.setRowCount(len(list_company))

        sorting_enable = self.tableWidget_stockScreener.isSortingEnabled()
        self.tableWidget_stockScreener.setSortingEnabled(False)
        for idx_row, company in enumerate(list_company):
            for key in company.keys():
                try:
                    idx_column = list_column_table.index(key)
                    assert (idx_column > 0 or idx_column < self.tableWidget_stockScreener.rowCount()), \
                        'Problem index of column when insert new row'
                    # create new row
                    #cell = QtGui.QTableWidgetItem()
                    cell = ValueTableItem.value_tableitem()
                    # we don't want user can change value of cell in table
                    cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
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

    def create_connection_signal_slot(self):
        """
        Add connection between signal (ex:click button) and slot (action to do, ex: open dialog box)
        :return: None
        """
        # sort column checkbox of table stock screnner
        self.tableWidget_stockScreener.horizontalHeader().sectionClicked\
            .connect(Slots.sort_column_checkbox_table_widget_stock_screener)
        # checked or unchecked the checkbox of cell clicked
        self.tableWidget_stockScreener.cellClicked.connect(Slots.modify_checkbox_table_widget_stock_screener)
        # connection btn Add to portfolio of Stock Screener
        self.btn_stockScreener_addPortfolio.clicked.connect(Slots.add_company_to_portfolio_stock_screener)
        # connection combo box line edit to portfolio of Stock Screener to same fct of btn Add to portfolio
        self.comboBox_stockScreener_portfolio.lineEdit().returnPressed\
            .connect(Slots.add_company_to_portfolio_stock_screener)
        # link slider and spin box of box layout to left
        HelperFunctionQt.link_spin_slider_layout(self.verticalLayout_left)
        # link slider and spin box of box layout to right
        HelperFunctionQt.link_spin_slider_layout(self.verticalLayout_right)
        # btn select criteria stock sceenner
        self.btn_selectAllCriteria.clicked.connect(Slots.select_all_criteria_stock_screener)
        # btn deselect criteria stock sceenner
        self.btn_deselectAllCriteria.clicked.connect(Slots.deselect_all_criteria_stock_screener)

    def add_portfolio_name_in_combobox(self, tab_widget_name, combobox_name):
        """
        Add portfolio name of DB in combo box chosen
        :param tab_widget_name: name of tabular widget (tabStockScreener, tabPortfolioManager, tabSimmulator)
        :type tab_widget_name: str
        :param combobox_name: name of combo box we want add portfolio name
        :type combobox_name: str
        :return: None
        """
        tab_widget = self.tab.findChild(QtGui.QWidget, tab_widget_name)
        cb = tab_widget.findChild(QtGui.QComboBox, combobox_name)

        list_portfolio = ManagerPortfolio.get_all_portfolio_info()
        for dict_portfolio in list_portfolio:
            cb.addItem(dict_portfolio.get('name'))


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

        # TODO: Check if OK to do that
        # When a click is made on a column's name, a sorting is done. We are changing the indicator in MainWindow
        # accordingly. The ValueTableItems that we are using use that indicator to adjust their comparison's algorithms.
        if table_widget.horizontalHeader().sortIndicatorOrder() == 0:
            Ui_MainWindow.is_descending = True
        else:
            Ui_MainWindow.is_descending = False

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

    @staticmethod
    def add_company_to_portfolio_stock_screener():
        """
        Get all information to add companies in portfolio with call function
        HelperFunctionQt.add_companies_to_portfolio_db
        :return: None
        """
        table_widget = ui.tableWidget_stockScreener
        if table_widget.rowCount() > 0:
            list_company = []
            for idx in range(table_widget.rowCount()):
                # get checkbox widget
                cb = HelperFunctionQt.get_widget_of_layout(
                                                table_widget.cellWidget(idx, table_widget.columnCount() - 1).layout(),
                                                QtGui.QCheckBox)
                if cb.isChecked():
                    # add symbol company in list company to add in DB for a portfolio
                    list_company.append(table_widget.item(idx, 1).text())
            # get name portfolio
            portfolio_name = ui.comboBox_stockScreener_portfolio.lineEdit().text()
            # add company to portfolio in db
            HelperFunctionQt.add_companies_to_portfolio_db(portfolio_name, list_company)

    @staticmethod
    def select_all_criteria_stock_screener():
        """
        Select all criteria of stock screener
        :return: None
        """
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_left, QtCore.Qt.Checked)
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_right, QtCore.Qt.Checked)

    @staticmethod
    def deselect_all_criteria_stock_screener():
        """
        Deselect all criteria of stock screener
        :return: None
        """
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_left, QtCore.Qt.Unchecked)
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_right, QtCore.Qt.Unchecked)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = ManagerMainWindow()
    ui.setupUi(MainWindow)

    ui.setup_manager()
    ui.setup_size_fixed()
    ui.create_data_table_stock_screener()
    ui.create_connection_signal_slot()

    MainWindow.show()
    sys.exit(app.exec_())
