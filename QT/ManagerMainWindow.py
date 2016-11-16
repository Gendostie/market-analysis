#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from QT.MainWindow import Ui_MainWindow
from QT.ManagerTest import ManagerTest
from Manager_DB import ManagerPortfolio, ManagerCompany
from QT import HelperFunctionQt
from QT.Singleton import Singleton

dict_type_simulation = {'Technical Analysis': 'technical_analysis_windows', 'By Low Set High': 'by_low_set_high',
                        'Global Ranking': 'global_ranking', '1$ For Each Company': ''}


class ManagerMainWindow(Ui_MainWindow):
    def setup_size_fixed(self):
        """
        Put min and max size of widget like main window for size fixed in setup Ui_MainWindow
        :return: None
        """
        # fixed size main window
        MainWindow.setMaximumSize(MainWindow.size())
        MainWindow.setMinimumSize(MainWindow.size())
        # adjust size tab
        self.tab.setMinimumSize(self.tab.size())
        self.tab.setMaximumSize(self.tab.size())
        # adjust column of table widget
        self.tableWidget_stockScreener.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableWidget_portfolio.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_manager(self):
        """
        Setup for widget already in MainWindow.ui to modify
        :return: None
        """
        # Stock Screener
        # Set min max criteria Stock Screener
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_left)
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_right)
        self.create_data_table_stock_screener()
        # Add placeholder to combobox portfolio Stock screener
        self.comboBox_stockScreener_portfolio.lineEdit().setPlaceholderText("Choose your portfolio name.")
        self.create_combobox_portfolio('tab_stockScreener', 'comboBox_stockScreener_portfolio')
        # Portfolio Manager
        self.comboBox_portfolioManager_portfolio.lineEdit().setPlaceholderText("Choose your portfolio name.")
        self.create_combobox_portfolio('tab_portfolioManager', 'comboBox_portfolioManager_portfolio')
        if self.comboBox_portfolioManager_portfolio.count() > 0:
            self.refresh_data_table_portfolio()
        self.create_combobox_company_portfolio_manager()
        # Simulator
        # Set min max criteria Simulator
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_left_2)
        HelperFunctionQt.set_min_max_slider_layout(self.verticalLayout_right_2)
        # Set min max datetime Simulator
        self.get_min_max_date_historic()
        # Add items of combobox type_simulation who be in list_type_simulation
        self.comboBox_typeSimulation.addItems(sorted(list(dict_type_simulation.keys())))

    def create_data_table_stock_screener(self):
        """
        Create data in table widget stock screener with data SQL
        :return: None
        """
        list_column_table = ['company_name', 'symbol', 'Revenue (Mil)', 'Net Income (Mil)',
                             'Gross Margin (%)', 'Dividends',
                             'Div. Yield (%)', 'EPS', 'P/E Ratio',
                             'BVPS', 'P/B Ratio', 'FCFPS', 'Close', '52wk (%)', 'Global Ranking']

        dict_company = ManagerCompany.get_historic_value_all_company()
        dict_params = self.get_all_min_max_criteria(self.horizontalLayout)

        max_nb_company = len(dict_company)
        dict_company = HelperFunctionQt.reduce_table(dict_company, dict_params)
        dict_company = HelperFunctionQt.calculate_global_ranking(dict_company, dict_params)
        self.lineEdit_nb_company.setText('%s/%s' % (str(len(dict_company)), str(max_nb_company)))

        if self.tableWidget_stockScreener.rowCount() < len(dict_company):
            self.tableWidget_stockScreener.setRowCount(len(dict_company))

        sorting_enable = self.tableWidget_stockScreener.isSortingEnabled()
        self.tableWidget_stockScreener.setSortingEnabled(False)
        for idx_row, company in enumerate(dict_company):
            for key in company.keys():
                try:
                    idx_column = list_column_table.index(key)
                    assert (idx_column > 0 or idx_column < self.tableWidget_stockScreener.rowCount()), \
                        'Problem index of column when insert new row'
                    # create new cell
                    HelperFunctionQt.create_new_cell_item_table_widget(self.tableWidget_stockScreener,
                                                                       idx_row, idx_column, company.get(key))
                except ValueError:
                    continue  # if column no exists in table stock screener, we continue
            # create cell with checkbox in last column
            cb = QtGui.QCheckBox()
            HelperFunctionQt.create_new_cell_widget_table_widget(self.tableWidget_stockScreener,
                                                                 idx_row,
                                                                 self.tableWidget_stockScreener.columnCount() - 1,
                                                                 cb)
        self.tableWidget_stockScreener.setSortingEnabled(sorting_enable)

    def create_connection_signal_slot(self):
        """
        Add connection between signal (ex:click button) and slot (action to do, ex: open dialog box)
        :return: None
        """
        # refresh combobox portfolio when we change tab widget, because we could be adding new portfolio
        self.tab.currentChanged.connect(Slots.refresh_combobox_portfolio_tab_widget)
        # Stock Screener
        # sort column checkbox of table stock screener
        self.tableWidget_stockScreener.horizontalHeader().sectionClicked \
            .connect(Slots.sort_column_checkbox_table_widget_stock_screener)
        # checked or unchecked the checkbox of cell clicked
        self.tableWidget_stockScreener.cellClicked.connect(Slots.modify_checkbox_table_widget_stock_screener)
        # connection btn Add to portfolio of Stock Screener
        self.btn_stockScreener_addPortfolio.clicked.connect(Slots.add_company_to_portfolio_stock_screener)
        # connection combo box line edit to portfolio of Stock Screener to same fct of btn Add to portfolio
        self.comboBox_stockScreener_portfolio.lineEdit().returnPressed \
            .connect(Slots.add_company_to_portfolio_stock_screener)
        # link slider and spin box of box layout to left
        HelperFunctionQt.link_spin_slider_layout(self.verticalLayout_left)
        # link slider and spin box of box layout to right
        HelperFunctionQt.link_spin_slider_layout(self.verticalLayout_right)
        # btn select criteria stock sceenner
        self.btn_selectAllCriteria.clicked.connect(Slots.select_all_criteria_stock_screener)
        # btn deselect criteria stock sceenner
        self.btn_deselectAllCriteria.clicked.connect(Slots.deselect_all_criteria_stock_screener)
        # connection btn Add to portfolio of Portfolio Manager
        self.btn_addCompany.clicked.connect(Slots.add_company_to_portfolio_portfolio_manager)
        # connection combo box line edit to portfolio of Portfolio Manager to same fct of btn Add to portfolio
        self.comboBox_portfolioManager_addCompany.lineEdit().returnPressed \
            .connect(Slots.add_company_to_portfolio_portfolio_manager)
        # Refresh table and global ranking depending on criteria selected
        self.btn_RefreshTableStockScreener.clicked.connect(Slots.refresh_table_stock_screener)

        # Portfolio Manager
        # connection btn Add to portfolio of Portfolio Manager
        self.btn_portfolio_ok.clicked.connect(self.refresh_data_table_portfolio)
        # connection combo box line edit to portfolio of Portfolio Manager to same fct of btn Add to portfolio
        self.comboBox_portfolioManager_portfolio.lineEdit().returnPressed \
            .connect(self.refresh_data_table_portfolio)
        self.comboBox_portfolioManager_portfolio.currentIndexChanged.connect(self.refresh_data_table_portfolio)
        # checked or unchecked the checkbox of cell clicked
        self.tableWidget_portfolio.cellClicked.connect(Slots.modify_checkbox_table_widget_portfolio_manager)
        # sort column checkbox of table portfolio
        self.tableWidget_portfolio.horizontalHeader().sectionClicked \
            .connect(Slots.sort_column_checkbox_table_widget_portfolio_manager)
        # delete companies selected of portfolio current
        self.btn_portfolio_delete_company_selected.clicked.connect(Slots.deleted_company_selected_table_portfolio)

        # Simulator
        # btn select criteria Simulator
        self.btn_selectAllCriteria_2.clicked.connect(Slots.select_all_criteria_simulator)
        # btn deselect criteria Simulator
        self.btn_deselectAllCriteria_2.clicked.connect(Slots.deselect_all_criteria_simulator)
        # connect min max datetime
        self.dateEdit_simulatorFrom.dateTimeChanged.connect(self.dateEdit_simulatorTo.setMinimumDateTime)
        self.dateEdit_simulatorTo.dateTimeChanged.connect(self.dateEdit_simulatorFrom.setMaximumDateTime)
        # btn for open pop-up to set params within type simulator selected
        self.btn_setParamsSimulation.clicked.connect(Slots.open_windows_setting_params_simulation)
        # btn for start simulation
        self.btn_startSimulation.clicked.connect(Slots.start_simulation)
        # btn for show report of simulation
        self.btn_showReport.clicked.connect(Slots.show_report)

    def create_combobox_portfolio(self, tab_widget_name, combobox_name):
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

    @staticmethod
    def get_all_min_max_criteria(horizontal_layout):
        """
        Get all min and max checked in layout horizontal criteria who content vertical layout left and right for
        tab Stock Screener or Portfolio Manager
        :param horizontal_layout: layout horizontal criteria who content vertical layout left and right
        :type horizontal_layout: QtGui.QBoxLayout
        :return: dict of criteria checked
        :rtype: dict{dict}
        """
        dict_min_max = {}
        # layout left
        layout = HelperFunctionQt.get_widget_of_layout(horizontal_layout, QtGui.QLayout)
        dict_min_max.update(HelperFunctionQt.get_min_max_layout_checked(layout))
        # layout right
        layout = HelperFunctionQt.get_widget_of_layout(horizontal_layout, QtGui.QLayout, 1)
        dict_min_max.update(HelperFunctionQt.get_min_max_layout_checked(layout))
        return dict_min_max

    def get_min_max_date_historic(self):
        min_datetime, max_datetime = ManagerCompany.get_minimum_maximum_value_date_historical()
        self.dateEdit_simulatorFrom.setDateTimeRange(QtCore.QDateTime(min_datetime), QtCore.QDateTime(max_datetime))
        self.dateEdit_simulatorTo.setDateTimeRange(QtCore.QDateTime(min_datetime), QtCore.QDateTime(max_datetime))
        self.dateEdit_simulatorTo.setDateTime(QtCore.QDateTime(max_datetime))

    def create_combobox_company_portfolio_manager(self):
        list_company = ManagerCompany.get_snp500()

        for company in list_company:
            self.comboBox_portfolioManager_addCompany.addItem(company.get("symbol") + " " + company.get("name"))

    def refresh_data_table_portfolio(self):
        """
        Refresh data of table portfolio depending on portfolio chosen
        :return: None
        """
        list_column_table = ['name', 'symbol']

        # get name portfolio
        self.tableWidget_portfolio.setRowCount(0)
        portfolio_name = self.comboBox_portfolioManager_portfolio.lineEdit().text()
        if portfolio_name == '' or portfolio_name is None:
            self.frame_managerPortfolio.setEnabled(False)
            # self.tableWidget_portfolio.clearContents()
            return 0  # no portfolio name
        else:
            # Refresh combo box if is new
            if ui.comboBox_portfolioManager_portfolio.findText(portfolio_name) == -1:
                ui.comboBox_portfolioManager_portfolio.addItem(portfolio_name)
            self.frame_managerPortfolio.setEnabled(True)

        # add portfolio if is new
        portfolio_id = ManagerPortfolio.create_portfolio(portfolio_name)[0].get('id_portfolio')[0]
        self.lineEdit_noPortfolio.setText(str(portfolio_id))  # set id portfolio to line edit

        list_company = ManagerPortfolio.get_companies_to_portfolio(portfolio_id)

        if self.tableWidget_portfolio.rowCount() < len(list_company):
            self.tableWidget_portfolio.setRowCount(len(list_company))

        sorting_enable = self.tableWidget_portfolio.isSortingEnabled()
        self.tableWidget_portfolio.setSortingEnabled(False)
        for idx_row, company in enumerate(list_company):
            for key in company.keys():
                try:
                    idx_column = list_column_table.index(key)
                    assert (idx_column > 0 or idx_column < self.tableWidget_portfolio.rowCount()), \
                        'Problem index of column when insert new row'
                    # create new cell
                    HelperFunctionQt.create_new_cell_item_table_widget(self.tableWidget_portfolio,
                                                                       idx_row, idx_column, company.get(key))
                except ValueError:
                    continue  # if column no exists in table stock screener, we continue
            # create cell with checkbox in last column
            cb = QtGui.QCheckBox()
            HelperFunctionQt.create_new_cell_widget_table_widget(self.tableWidget_portfolio,
                                                                 idx_row,
                                                                 self.tableWidget_portfolio.columnCount() - 1,
                                                                 cb)
        self.tableWidget_portfolio.setSortingEnabled(sorting_enable)


class Slots:
    @staticmethod
    def modify_checkbox_table_widget_stock_screener(row, column):
        """
        Give possibility to user to click cell of checkbox fo checked or unchecked case
        :param row: row cell clicked
        :type row: int
        :param column: column of cell clicked
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
            Singleton.set_order(Singleton(), True)
        else:
            Singleton.set_order(Singleton(), False)

        if column == table_widget.columnCount() - 1:
            HelperFunctionQt.sorted_column_checkbox_table_widget(table_widget)

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
            # Refresh combo box if is new
            if ui.comboBox_stockScreener_portfolio.findText(portfolio_name) == -1:
                ui.comboBox_stockScreener_portfolio.addItem(portfolio_name)

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

    @staticmethod
    def refresh_combobox_portfolio_tab_widget(idx):
        """
        Refresh data in combobox of tab widget current
        :param idx: index of tab widget
        :type idx: int
        :return: None
        """
        tab_widget = ui.tab.widget(idx)
        name_tab_widget = tab_widget.objectName()
        cb = tab_widget.findChild(QtGui.QComboBox, 'comboBox_' + name_tab_widget[len('tab_'):] + '_portfolio')

        if cb is None:
            return 0  # no combobox portfolio find in tab widget

        cb.clear()  # clear all item of combobox
        list_portfolio = ManagerPortfolio.get_all_portfolio_info()
        for dict_portfolio in list_portfolio:
            cb.addItem(dict_portfolio.get('name'))

    @staticmethod
    def modify_checkbox_table_widget_portfolio_manager(row, column):
        """
        Give possibility to user to click cell of checkbox fo checked or unchecked case
        :param row: row cell clicked
        :type row: int
        :param column: column of cell clicked
        :type column: int
        :return: None
        """
        if column == ui.tableWidget_portfolio.columnCount() - 1:
            # get checkbox widget
            cb = ui.tableWidget_portfolio.cellWidget(row, column).layout().itemAt(0).widget()
            cb.setChecked(not cb.isChecked())

    @staticmethod
    def sort_column_checkbox_table_widget_portfolio_manager(column):
        """
        Sorted column with checkbox, ascending = Unchecked to Checked ; descending = Checked to Unchecked
        :param column: column of header cell clicked
        :type column: int
        :return: None
        """
        if column == ui.tableWidget_portfolio.columnCount() - 1:
            HelperFunctionQt.sorted_column_checkbox_table_widget(ui.tableWidget_portfolio)

    @staticmethod
    def add_company_to_portfolio_portfolio_manager():
        """
        Add company selected to portfolio selected with call function HelperFunctionQt.add_companies_to_portfolio_db
        :return: None
        """
        company = ui.comboBox_portfolioManager_addCompany.lineEdit().text().split()
        # get name portfolio
        portfolio_name = ui.comboBox_portfolioManager_portfolio.lineEdit().text()
        # add company to portfolio in db
        HelperFunctionQt.add_companies_to_portfolio_db(portfolio_name, [company[0]])
        # refresh table portfolio manager
        ui.refresh_data_table_portfolio()

    @staticmethod
    def deleted_company_selected_table_portfolio():
        table_widget = ui.tableWidget_portfolio
        if table_widget.rowCount() > 0:
            list_company_deleted = []
            for idx in range(table_widget.rowCount()):
                # get checkbox widget
                cb = HelperFunctionQt.get_widget_of_layout(
                    table_widget.cellWidget(idx, table_widget.columnCount() - 1).layout(),
                    QtGui.QCheckBox)
                if cb.isChecked():
                    # add symbol company in list company to delete in DB for a portfolio
                    list_company_deleted.append(table_widget.item(idx, 1).text())
            # get name portfolio
            portfolio_id = ui.lineEdit_noPortfolio.text()
            # add company to portfolio in db
            HelperFunctionQt.delete_companies_to_portfolio_db(portfolio_id, list_company_deleted)
            # refresh table portfolio
            ui.refresh_data_table_portfolio()

    @staticmethod
    def refresh_table_stock_screener():
        ui.tableWidget_stockScreener.setRowCount(0)
        ui.create_data_table_stock_screener()

    @staticmethod
    def select_all_criteria_simulator():
        """
        Select all criteria of stock screener
        :return: None
        """
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_left_2, QtCore.Qt.Checked)
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_right_2, QtCore.Qt.Checked)

    @staticmethod
    def deselect_all_criteria_simulator():
        """
        Deselect all criteria of stock screener
        :return: None
        """
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_left_2, QtCore.Qt.Unchecked)
        HelperFunctionQt.select_deselect_combobox_layout(ui.verticalLayout_right_2, QtCore.Qt.Unchecked)

    # TODO: to completed
    @staticmethod
    def open_windows_setting_params_simulation():
        print('Open pop-up to set params type simulation selected')
        type_simulation_selected = ui.comboBox_typeSimulation.currentText()
        print(type_simulation_selected)
        Dialog = QtGui.QDialog()
        dl = ManagerTest()
        dl.setupUi(Dialog)
        # dl.buttonBox.accepted.connect(Slots.get_value_params)

        if Dialog.exec():
            print(dl.get_values())

    # TODO: to completed
    @staticmethod
    def start_simulation():
        print('Start simulation')

    # TODO: to completed
    @staticmethod
    def show_report():
        print('Show report simulation')

    # TODO: to completed
    @staticmethod
    def get_value_params():
        print(0)

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = ManagerMainWindow()
    ui.setupUi(MainWindow)

    ui.setup_manager()
    ui.setup_size_fixed()
    ui.create_connection_signal_slot()

    MainWindow.show()
    sys.exit(app.exec_())
