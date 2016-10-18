#-------------------------------------------------
#
# Project created by QtCreator 2016-10-03T11:25:30
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = market-analysis_qt
TEMPLATE = app

CONFIG  += \
    no_keywords\
    qt

SOURCES += \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h

FORMS   += \
    mainwindow.ui

INCLUDEPATH += \
    /usr/include/python34

LIBS    += \
    -lpython34 \
    -LC:\Python34\libs

#DISTFILES += \
#    ../../Manager_DB/DbConnection.py \
#    ../../Manager_DB/ManagerCompany.py \
#    ../../Manager_DB/ManagerPortfolio.py
