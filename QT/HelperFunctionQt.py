import io
import pandas as pd
from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates

from MainWindow import _translate
from Manager_DB import ManagerPortfolio
import ValueTableItem
from Singleton import divide

dict_criteria = {'Adj. Close': 'close_val',
                 'Revenue (Mil)': 'revenu_usd_mil',
                 'Net Income (Mil)': 'net_income_usd_mil',
                 'Gross Margin (%)': 'gross_margin_pct',
                 'Dividends': 'dividends_usd',
                 'EPS': 'earning_per_share_usd',
                 'BVPS': 'book_value_per_share_usd',
                 'FCFPS': 'free_cash_flow_per_share_usd',
                 'Div. Yield (%)': 'dividend_yield',
                 'P/E Ratio': 'p_e_ratio',
                 'P/B Ratio': 'p_b_ratio',
                 '52wk (%)': '52wk'}


def get_row_table_widget(table_widget, idx_row):
    """
    Get row in table widget
    :param table_widget: table qt
    :type table_widget: QtGui.QTableWidget
    :param idx_row: index of row
    :type idx_row: int
    :return: row qt, list of cell item and/or cell widget
    :rtype: list[QtGui.QTableWidgetItem]
    """
    row_items = []
    for idx in range(table_widget.columnCount()):
        if isinstance(table_widget.item(idx_row, idx), QtGui.QTableWidgetItem):
            row_items.append(table_widget.takeItem(idx_row, idx))
        else:
            row_items.append(table_widget.cellWidget(idx_row, idx))
    return row_items


def set_row_table_widget(table_widget, row_items):
    """
    Add row in end of table widget
    :param table_widget: table qt
    :type table_widget: QtGui.QTableWidget
    :param row_items: row of table widget
    :type row_items: list[QtGui.QTableWidgetItem]
    :return: None
    """
    table_widget.setRowCount(table_widget.rowCount() + 1)
    for idx_column, item in enumerate(row_items):
        if isinstance(item, QtGui.QTableWidgetItem):
            table_widget.setItem(table_widget.rowCount()-1, idx_column, item)
        elif item is None:
            pass
        else:
            table_widget.setCellWidget(table_widget.rowCount()-1, idx_column, item)


def get_widget_of_layout(layout, type_object_to_find, nb_same_type_skip=0):
    """
    Search and find object in layout
    :param layout: layout where object we search is
    :type layout: QtGui.QBoxLayout
    :param type_object_to_find: type Qt to find, ex: QCheckbox
    :type type_object_to_find: Object QtGui
    :param nb_same_type_skip: optional, if we have must one object of same type in layout, we can specify how much
                                object to skip before get the good object
    :type nb_same_type_skip: int
    :return: object qt we search or None if not found
    :rtype: Object QtGui, None
    """
    return_object = None
    nb_object_skipped = 0
    if isinstance(layout, QtGui.QBoxLayout):
        # just one item in box layout
        if layout.count() == 1:
            # object direct
            if isinstance(layout.itemAt(0), type_object_to_find):
                return_object = layout.itemAt(0)
            # check if box layout in box layout
            elif isinstance(layout.itemAt(0), QtGui.QBoxLayout):
                # call recursive to get object we search in box layout
                return_object = get_widget_of_layout(layout, type_object_to_find)
            # check if widget item in box layout
            elif isinstance(layout.itemAt(0), QtGui.QWidgetItem):
                # extract object of widget
                if isinstance(layout.itemAt(0).widget(), type_object_to_find):
                    return_object = layout.itemAt(0).widget()
        elif layout.count() > 1:
            # check in all object in box layout
            for i in range(layout.count()):
                # object direct
                if isinstance(layout.itemAt(i), type_object_to_find):
                    return_object = layout.itemAt(i)
                # check if box layout in box layout
                elif isinstance(layout.itemAt(i), QtGui.QBoxLayout):
                    # call recursive to get object we search in box layout
                    return_object = get_widget_of_layout(layout, type_object_to_find)
                # check if widget item in box layout
                elif isinstance(layout.itemAt(i), QtGui.QWidgetItem):
                    # extract object of widget
                    if isinstance(layout.itemAt(i).widget(), type_object_to_find):
                        return_object = layout.itemAt(i).widget()
                # object is found and nb object to skip is done
                if return_object and nb_same_type_skip == nb_object_skipped:
                    break
                elif return_object and nb_same_type_skip != nb_object_skipped:
                    return_object = None  # re-init object
                    nb_object_skipped += 1
        else:
            raise ValueError("No object in box layout.")
    else:
        raise TypeError("Layout must be a QBoxLayout")

    if not isinstance(return_object, type_object_to_find):
        raise ValueError("No object we search in box layout.")
    return return_object


def add_companies_to_portfolio_db(portfolio_name, list_company, db):
    """
    Call function for add company to portfolio in db
    :param portfolio_name: name of portfolio
    :type portfolio_name: str
    :param list_company: list symbol of company
    :type list_company: list[str]
    :param db: connection to db
    :type db: DbConnection.DbConnection
    :return: None
    """
    # add portfolio if is new
    portfolio_id = ManagerPortfolio.create_portfolio(portfolio_name, db)
    # add company to portfolio in db
    nb_company_added = ManagerPortfolio.add_companies_to_portfolio(portfolio_id[0].get('id_portfolio')[0],
                                                                   list_company, db)
    print("Nb company added: %s" % nb_company_added)


def select_deselect_combobox_layout(layout, is_checked):
    """
    Common function for selected or deselected combo box in a layout
    :param layout: Widget layout, must be a simple layout in layout
    :type layout: QtGui.QLayout
    :param is_checked: 2 if checked or 0 for unchecked
    :type is_checked: int
    :return: None
    """
    if layout.count() > 0:
        for idx in range(layout.count()):
            cb = get_widget_of_layout(layout.itemAt(idx), QtGui.QCheckBox)
            if cb:
                cb.setCheckState(is_checked)


def link_spin_slider_layout(layout):
    """
    Common function for link (connect signal/slot) spin box and slider
    :param layout: Widget layout, must be a simple layout in layout
    :type layout: QtGui.QLayout
    :return: None
    """
    for idx_layout in range(layout.count()):
        # link min
        min_spin_box = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QDoubleSpinBox)
        min_range_slider = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QSlider)
        min_spin_box.valueChanged.connect(min_range_slider.setValue)
        min_range_slider.valueChanged.connect(min_spin_box.setValue)
        # link max
        max_spin_box = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QDoubleSpinBox, 1)
        max_range_slider = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QSlider, 1)
        max_spin_box.valueChanged.connect(max_range_slider.setValue)
        max_range_slider.valueChanged.connect(max_spin_box.setValue)

        min_spin_box.valueChanged.connect(max_spin_box.setMinimum)
        max_spin_box.valueChanged.connect(min_spin_box.setMaximum)

        min_range_slider.valueChanged.connect(max_range_slider.setMinimum)
        max_range_slider.valueChanged.connect(min_range_slider.setMaximum)


# TODO: Create a DbConnection Object
def set_min_max_slider_layout(layout, dict_min_max_value_criteria_calc):
    """
    Set value min and max of QSlider of layout attribute
    :param layout: Widget layout, must be a simple layout in layout
    :type layout: QtGui.QLayout
    :param dict_min_max_value_criteria_calc: dict of value min and max of criteria we must calculate
    :type dict_min_max_value_criteria_calc: dict{dict}
    :return: None
    """
    for idx_layout in range(layout.count()):
        # Layout of the attribute
        layout_attr = layout.itemAt(idx_layout)
        # Name of the attribute
        name_attr = layout_attr.itemAt(0).widget().text()
        if name_attr in dict_criteria.keys():
            name_attr_db = dict_criteria[name_attr]
            min_val = dict_min_max_value_criteria_calc[name_attr_db].get('min', 0)
            max_val = dict_min_max_value_criteria_calc[name_attr_db].get('max', 0)
        else:
            continue

        # Min value
        min_spin_box = get_widget_of_layout(layout_attr, QtGui.QDoubleSpinBox)
        min_range_slider = get_widget_of_layout(layout_attr, QtGui.QSlider)

        min_spin_box.setMinimum(min_val)
        min_spin_box.setMaximum(max_val)
        min_spin_box.setValue(min_val)
        min_range_slider.setMinimum(min_val)
        min_range_slider.setMaximum(max_val)
        min_range_slider.setValue(min_val)

        # Max value
        max_spin_box = get_widget_of_layout(layout_attr, QtGui.QDoubleSpinBox, 1)
        max_range_slider = get_widget_of_layout(layout_attr, QtGui.QSlider, 1)

        max_spin_box.setMinimum(min_val)
        max_spin_box.setMaximum(max_val)
        max_spin_box.setValue(max_val)
        max_range_slider.setMinimum(min_val)
        max_range_slider.setMaximum(max_val)
        max_range_slider.setValue(max_val)

        # Dividends is float
        if name_attr == 'Dividends' or name_attr == 'Div. Yield (%)':
            min_spin_box.setDecimals(2)
            min_spin_box.setSingleStep((max_val-min_val)/100)
            max_spin_box.setDecimals(2)
            max_spin_box.setSingleStep((max_val-min_val)/100)


def create_new_cell_item_table_widget(table_widget, idx_row, idx_column, value):
    """
    Create a cell item in row to column specify of table widget chosen
    :param table_widget: table qt
    :type table_widget: QtGui.QTableWidget
    :param idx_row: index of row
    :type idx_row: int
    :param idx_column: index of column
    :type idx_column: int
    :param value: value to display in cell
    :type value: str
    :return: None
    """
    # create new row
    cell = ValueTableItem.ValueTableItem()
    # we don't want user can change value of cell in table QtCore.Qt.ItemIsEditable
    cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

    value = value if value is not None else ""
    if idx_column > 1:
        cell.setTextAlignment(QtCore.Qt.AlignRight + QtCore.Qt.AlignVCenter)

    cell.setText(_translate("MainWindow", str(value), None))
    table_widget.setItem(idx_row, idx_column, cell)


def create_new_cell_widget_table_widget(table_widget, idx_row, idx_column, widget_of_widget):
    """
    Create a cell widget with a other widget (ex: checkbox)
    :param table_widget: table qt
    :type table_widget: QtGui.QTableWidget
    :param idx_row: index of row
    :type idx_row: int
    :param idx_column: index of column
    :type idx_column: int
    :param widget_of_widget: widget to display in cell (ex: checkbox)
    :type widget_of_widget: QtGui.QWidget(QtGui.QWidget)
    :return: None
    """
    widget = QtGui.QWidget()

    h_box_layout = QtGui.QHBoxLayout()
    h_box_layout.setMargin(1)
    h_box_layout.setAlignment(QtCore.Qt.AlignCenter)
    h_box_layout.addWidget(widget_of_widget)

    widget.setLayout(h_box_layout)
    table_widget.setCellWidget(idx_row, idx_column, widget)


def sorted_column_checkbox_table_widget(table_widget):
    """
    Sorted column with checkbox, ascending = Unchecked to Checked ; descending = Checked to Unchecked
    :param table_widget: table qt
    :type table_widget: QtGui.QTableWidget
    :return: None
    """
    column = table_widget.columnCount() - 1
    # sort_order = 0 => ascending ; Qt::Unchecked = 0  Qt::Checked = 2  Qt::PartiallyChecked = 1
    sort_order = table_widget.horizontalHeader().sortIndicatorOrder()
    # sort_indicator = table_widget.horizontalHeader().sortIndicatorSection()
    # put value of same scale of checkbox state
    sort_order = 2 if sort_order == 1 else sort_order
    if table_widget.rowCount() > 0:
        list_row_remove = []
        for idx in range(table_widget.rowCount()):
            # get checkbox widget
            cb = get_widget_of_layout(table_widget.cellWidget(idx, column).layout(), QtGui.QCheckBox)
            if cb.checkState() != sort_order:
                row = get_row_table_widget(table_widget, idx)
                set_row_table_widget(table_widget, row)
                list_row_remove.append(idx)
        list_row_remove.reverse()
        for idx in list_row_remove:
            table_widget.removeRow(idx)
    sort_order = 1 if sort_order == 2 else sort_order  # put value of sort state
    table_widget.horizontalHeader().setSortIndicator(column, sort_order)  # set indicator column sort


def delete_companies_to_portfolio_db(portfolio_id, list_company, db):
    """
    Delete companies checked in table portfolio for deleted of bd for a portfolio_id specific
    :param portfolio_id: id of portfolio
    :type portfolio_id: int
    :param list_company: list of companies checked to deleted
    :type list_company: list[str]
    :param db: connection to db
    :type db: DbConnection.DbConnection
    :return: None
    """
    # delete companies to portfolio in db
    nb_company_deleted = ManagerPortfolio.delete_companies_to_portfolio(portfolio_id, list_company, db)
    print("Nb company deleted: %s" % nb_company_deleted)


def reduce_table(list_cie, dict_param):
    new_list_company = []
    for cie in list_cie:
        flag = True
        for name_param, params in dict_param.items():
            # If a value is None for a parameter that is checked, we remove the company.
            if cie[name_param] is not None:
                cie_val = float(cie[name_param])
            else:
                flag = False
                break
            # Check MIN
            if cie_val < params['min']:
                flag = False
                break
            # Check MAX
            elif cie_val > params['max']:
                flag = False
                break
        if flag:
            new_list_company.append(cie)

    return new_list_company


def calculate_global_ranking(list_company, dict_params):
    """
    Calculate global ranking for company
    :param list_company: list value for all company s&p500
    :type list_company: list[dict]
    :param dict_params: list criteria selected
    :type dict_params: dict[dict]
    :return: list value for all company s&p500 with adding global ranking
    :rtype: list[dict]
    """
    # Check if we have company
    if len(list_company) > 0:
        df_company = pd.DataFrame.from_dict(list_company).set_index(['symbol'])
    else:
        return list_company

    # init dict ranking
    dict_ranking_company = {}
    for symbol in df_company.axes[0]:
        dict_ranking_company[symbol] = 0

    # Delete param Close if exists
    if dict_params.get('Adj. Close'):
        dict_params.pop('Adj. Close')

    # Sum ranking params of company
    for param in dict_params:
        cpt = 1
        param_value_company = pd.to_numeric(df_company[param], errors='ignore').sort_values(ascending=False)
        for symbol in param_value_company.keys():
            dict_ranking_company[symbol] += cpt
            cpt += 1

    # Means of sum ranking and put in list_ci
    for company in list_company:
        global_ranking = 0
        if len(dict_params) != 0:
            global_ranking = divide(dict_ranking_company[company['symbol']], len(dict_params))
        if 0 <= float(global_ranking) <= len(list_company):
            company['Global Ranking'] = global_ranking
        else:
            print('Global ranking out range: %s, max: %s' % (global_ranking, len(list_company)))
    return list_company


def get_min_max_layout_checked(layout):
    """
    Get min and max checked in layout left or right
    :param layout: layout left or right
    :type layout: QtGui.QBoxLayout
    :return: dict of min max of layout
    :rtype: dict
    """
    dict_min_max = {}
    for idx_layout in range(layout.count()):
        if get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QCheckBox).isChecked():
            name_attr = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QCheckBox).text()
            min_val = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QDoubleSpinBox).text()
            max_val = get_widget_of_layout(layout.itemAt(idx_layout), QtGui.QDoubleSpinBox, 1).text()
            dict_min_max[name_attr] = {'min': float(min_val.replace(',', '.')), 'max': float(max_val.replace(',', '.'))}
    return dict_min_max


def get_params_simulation(parent_object):
    """
    Get params of simulation with a specific QWidget containing param. ex: QLayout, QFrame
    :param parent_object: Object contains children object who contains value
    :rtype parent_object: QtGui.QFrame | QtGui.QLayout
    :return: dictionary containing names of the values and their values
    :rtype: dict
    """
    return_res = {}
    for child in parent_object.children():
        # skip label of spinbox or line edit
        if isinstance(child, (QtGui.QDialogButtonBox, QtGui.QLabel, QtGui.QPushButton)):
            continue
        elif isinstance(child, QtGui.QComboBox):
            obj_text = child.currentText()
        elif isinstance(child, (QtGui.QDoubleSpinBox, QtGui.QSpinBox)):
            obj_text = child.value()
        else:
            obj_text = child.text()
        name_obj = child.objectName()  # get name of value
        return_res[name_obj[name_obj.rfind('_') + 1:]] = obj_text
    return return_res


def read_reference_curve(path_log_broker, in_list=False):
    """
    Read log of data of the reference curve and return in list the data
    :param path_log_broker: path of log who contains data for reference curve
    :type path_log_broker: str
    :return: list of list or DataFrame of Panda for value of portfolio of each open day
    :rtype: list[list] | pd.DataFrame
    """
    path_log_broker = path_log_broker.replace('log_brok', 'log_brok_ref')
    file = open(path_log_broker, 'r')
    if in_list:
        list_data = []
        for line in file:
            line = line.strip().split(';')
            list_data.append(line)
        return list_data
    else:
        return pd.read_csv(io.StringIO(file.read()), sep=';')


#########################################################################################################
#                                 Function to create and update plot QT
#########################################################################################################
def create_plot_qt(x_date, y_value, horizontal_layout_plot):
    """
    Create plot to display in interface qt in a layout box.
    :param x_date: list datetime associate to values in axis y
    :type x_date: list[datetime]
    :param y_value: list of value to display line of plot
    :type y_value: list[float]
    :param horizontal_layout_plot:
    :type horizontal_layout_plot: QtGui.QLayout
    :return: figure of plot
    :rtype: Figure
    """
    fig = Figure()
    axes = fig.add_subplot(111)
    axes.plot(x_date, y_value)
    if len(x_date) > 0:
        set_axes_fig_plot(axes, x_date[0], x_date[-1])
    fig.autofmt_xdate()

    canvas = FigureCanvas(fig)
    # Clear plot if exists already
    for i in range(horizontal_layout_plot.count()):
        horizontal_layout_plot.itemAt(i).widget().setParent(None)
    horizontal_layout_plot.addWidget(canvas)
    canvas.draw()

    return fig


def set_axes_fig_plot(axes, x_min, x_max):
    """
    Set axes to display label of axis and title of plot and
    :param axes: object axes
    :type axes: Axes of matplotlib
    :param x_min: datetime min
    :type x_min: datetime
    :param x_max: datetime max
    :type x_max: datetime
    :return: None
    """
    axes.set_xlim(x_min, x_max)
    axes.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
    axes.format_xdata = dates.DateFormatter('%Y-%m-%d')

    axes.set_title('Results of simulation')
    axes.set_xlabel('Dates')
    axes.set_ylabel('Values ($)')


def update_plot(fig, x_date, y_value, ref_curve):
    """
    Udate plot current of widget
    :param fig: object Figure
    :type fig: Figure
    :param x_date: list datetime associate to values in axis y
    :type x_date: list[datetime]
    :param y_value: list of value to display line of plot
    :type y_value: list[float]
    :param ref_curve: Data of reference curve for plot Qt simulation
    :type ref_curve: pandas.DataFrame
    :return: None
    """
    axes = fig.get_axes()[0]
    axes.cla()
    axes.plot(x_date, y_value)
    # axes.plot(list(ref_curve['date']), ref_curve.values)
    # TODO Calculate portfolio_value with ref_curve for ref_curv optimal
    axes.legend(['Simulation', 'Reference Curve'], loc='best')
    set_axes_fig_plot(axes, x_date[0], x_date[-1])
    fig.autofmt_xdate()
    fig.canvas.draw()
