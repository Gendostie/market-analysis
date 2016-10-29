#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

import ManagerPortfolio


def take_row_table_widget(table_widget, idx_row):
    """

    :param table_widget:
    :type table_widget: QtGui.QTableWidget
    :param idx_row:
    :type idx_row: int
    :return:
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

    :param table_widget:
    :type table_widget: QtGui.QTableWidget
    :param row_items:
    :type row_items: list[QtGui.QTableWidgetItem]
    :return:
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


def add_companies_to_portfolio_db(portfolio_name, list_company):
    """
    Call function for add company to portfolio in db
    :param portfolio_name: name of portfolio
    :type portfolio_name: str
    :param list_company: list symbol of company
    :type list_company: list[str]
    :return: None
    """
    # add portfolio if is new
    portfolio_id = ManagerPortfolio.create_portfolio(portfolio_name)
    # add company to portfolio in db
    nb_company_added = ManagerPortfolio.add_companies_to_portfolio(portfolio_id, list_company)
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