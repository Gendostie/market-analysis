#-------------------------------------------------
#
# Project created by QtCreator 2016-10-03T11:25:30
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = market-analysis_qt
TEMPLATE = app


SOURCES += main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h \

FORMS   += \
    mainwindow.ui

CONFIG  += \
    no_keywords

INCLUDEPATH += \
    /usr/include/python34

LIBS     += \
    -lpython34

DISTFILES += \
    ../../Manager_DB/DbConnection.py \
    ../../Manager_DB/ManagerCompany.py \
    ../../Manager_DB/ManagerPortfolio.py
