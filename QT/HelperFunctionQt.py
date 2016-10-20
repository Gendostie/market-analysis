#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui


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
