#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QCheckBox>
#include <QLineEdit>
#include <QSpacerItem>
#include <QHBoxLayout>
#include <QLabel>
#include <QTableWidgetItem>
#include <QtDebug>
#include <QCoreApplication>
#include <QApplication>
#include <QProcess>
#include <QDir>

#include <iostream>
#include "C:/Python34/include/Python.h"
//#include <Python.h>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    qDebug() << "python -c \"from Manager_DB.ManagerCompany import *; print(get_snp500())\"";
    QProcess process;
    process.start("python -c \"import ManagerCompany; print(ManagerCompany.get_snp500())\"", QIODevice::ReadOnly);
//    process.start("python -c \"from ManagerCompany import *; print(get_snp500())\"", QIODevice::ReadOnly);
    process.waitForFinished(); // Attente de la fin du processus python
    qDebug() << process.readAllStandardError();
    qDebug() << process.readAllStandardOutput();

//    QDir dir("market-analysis");
//    while(!dir.exists()){
//        dir = QDir(dir.path().prepend("../"));
//    }
//    qDebug() << dir.absolutePath();

//    std::ostringstream python_path;
//    python_path<<"sys.path.append(\"" + dir.absolutePath() + "\")";


//    create_data_table_stock_screener(ui->tableWidget_stockScreener);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::create_data_table_stock_screener(QTableWidget *tableWidget){
    //TODO: change for call sql
    QList<QStringList> *list_company = new QList<QStringList>;
    //QStringList l = new QStringList();
    QStringList l, l1;
    l << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE"
      << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE" << "GOOGLE";
    l1 << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON"
       << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON" << "AMAZON";
//    qDebug() << "length company: " << l.size();
//    qDebug() << "company: " << l;

    list_company->append(l);
    list_company->append(l1);
//    qDebug() << "length list_company: " << list_company->size();
//    qDebug() << "length list_company[0]: " << list_company[0].size();
//    for(int i = 0; i < list_company[0].size(); i++){
//        qDebug() << "length list_company[0][" << i << "]: " << list_company[0][i].size();
//        for(int j = 0; j < list_company[0][i].size(); j++){
//            qDebug() << "list_company[0][" << i << "]: " << list_company[0][i][j];
//        }
//    }

    if (tableWidget->rowCount() < list_company->size())
            tableWidget->setRowCount(list_company->size());

    const bool sorting_enabled = tableWidget->isSortingEnabled();
    tableWidget->setSortingEnabled(false);
    for(int i = 0; i < list_company->size(); i++){
        //create new row
        QTableWidgetItem *cell = new QTableWidgetItem();
        tableWidget->setVerticalHeaderItem(i, cell);

        for(int j = 0; j < list_company[0][i].size(); j++){
            QTableWidgetItem *cell = new QTableWidgetItem();
            //we don't want user can change value of cell in table
            cell->setFlags(Qt::ItemIsSelectable|Qt::ItemIsUserCheckable|Qt::ItemIsEnabled);
            cell->setText(QApplication::translate("MainWindow", list_company[0][i][j].toLatin1(), 0));
            tableWidget->setItem(i, j, cell);
        }
        //is last column, for checkbox
        Q_ASSERT_X(tableWidget->columnCount() - 1 == 13, "create_data_table_stock_screener",
                   QString("The index of column is more than 13, i = %1").arg(i).toLatin1());

        QWidget * widget_cb = new QWidget();
        QHBoxLayout *hBoxLayout_cb = new QHBoxLayout();
        QCheckBox *cb = new QCheckBox();
        hBoxLayout_cb->setMargin(1);
        hBoxLayout_cb->setAlignment(Qt::AlignCenter);
        hBoxLayout_cb->addWidget(cb);
        widget_cb->setLayout(hBoxLayout_cb);
        ui->tableWidget_stockScreener->setCellWidget(i, tableWidget->columnCount() - 1, widget_cb);
    }
    tableWidget->setSortingEnabled(sorting_enabled);
}


