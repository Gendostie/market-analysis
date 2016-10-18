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
#include <sstream>
#include "C:/Python34/include/Python.h"
//#include <Python.h>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

//    QString result = call_function_python("Manager_DB", "ManagerCompany", "get_company_by_symbol", "GOOGL");
//    QString result = call_function_python("Manager_DB", "ManagerCompany", "get_snp500", "GOOGL");
//    QString result = call_function_python("Manager_DB", "ManagerCompany", "get_historic_value_all_company", "");
//    qDebug() << result;
//    QList<QStringList> res_qsl = format_result_to_python(result);
//    for(int i = 0; i < res_qsl.size(); i++){
//        qDebug() << res_qsl[i];
//        for(int j = 0; j < res_qsl[i].size(); j++){
//            QString v = QString(res_qsl[i][j]);
//            qDebug() << v;
//        }
//    }

    create_data_table_stock_screener(ui->tableWidget_stockScreener);
}

MainWindow::~MainWindow()
{
    delete ui;
}

/**
 * @brief MainWindow::call_function_python use for call function python of python script
 * @param name_folder_file_py
 * @param name_python_file name of python file without extension .py, ex: ManagerCompany
 * @param name_fct function name to call, ex: get_snp500
 * @param args argument for function called, ex: for get_company_by_symbol(symbol, db=None), GOOGL
 * @return string of return values, ex: "[{'symbol': 'GOOGL', 'last_update_historic': None, 'name': 'Alphabet Inc Class A', 'is_in_snp500': '\\x01'}]\r\n"
 */
QString MainWindow::call_function_python(QString name_folder_file_py, QString name_python_file, QString name_fct, QString args){
    //find path of project
    QDir dir("market-analysis");
    while(!dir.exists()){
        dir = QDir(dir.path().prepend("../"));
    }

    QProcess cmd;
    cmd.start("python " + dir.absolutePath() + "/" + name_folder_file_py + "/" + name_python_file + ".py " + name_fct + " " + args);
    cmd.waitForFinished(); // wait end of processus

    QString err(cmd.readAllStandardError()); //error in process cmd
    if(!err.isEmpty())
        qFatal(err.toLatin1());

    return cmd.readAllStandardOutput(); //get result send by python function by print()
}

/**
 * @brief format_result_to_python
 * @param result result send by function python
 * @return list of list of string, ex: (("symbol: GOOGL", "last_update_historic: None", "name: Alphabet Inc Class A", "is_in_snp500: \\x01"))
 */
QList<QStringList> MainWindow::format_result_to_python(QString result){
    QStringList result_list = result.mid(result.indexOf("[{")+2, result.indexOf("}]")-2).replace("'", "").split("}, {");
    QList<QStringList> return_value;
    for(int i = 0; i < result_list.size(); i++){
        return_value.append(result_list.at(i).split(", "));
    }
    return return_value;
}

/**
 * @brief MainWindow::create_data_table_stock_screener add row in table of stock screener
 * @param tableWidget table send by reference
 */
void MainWindow::create_data_table_stock_screener(QTableWidget *tableWidget){
    QString result = call_function_python("Manager_DB", "ManagerCompany", "get_historic_value_all_company", "");
    qDebug() << result;
    QList<QStringList> *list_company = new QList<QStringList>(format_result_to_python(result));
//    for(int i = 0; i < list_company->size(); i++){
//        qDebug() << list_company[0][i];
//        for(int j = 0; j < list_company[0][i].size(); j++){
//            qDebug() << list_company[0][i][j];
//        }
//    }

    //Get order of colum with name retun_value of python function
    QStringList list_colum_table;
    list_colum_table << "company_name"  << "symbol" << "stock_value" << "income" << "gross_margin"
                     << "dividends" << "market_capitaisation" << "finantical_index" << "index_end" << "earning"
                     << "book_value" << "sales_value" << "cash_flow";

    if (tableWidget->rowCount() < list_company->size())
            tableWidget->setRowCount(list_company->size());

    //("cash_flow: None", "gross_margin: None", "book_value: None", "name: Agilent Technologies Inc", "revenue: None", "dividends: None", "symbol: A", "datetime_value: None", "income: None", "earning: None")
    const bool sorting_enabled = tableWidget->isSortingEnabled();
    tableWidget->setSortingEnabled(false);
    for(int i = 0; i < list_company->size(); i++){
        //create new row
        QTableWidgetItem *cell = new QTableWidgetItem();
        tableWidget->setVerticalHeaderItem(i, cell);

        for(int j = 0; j < list_company[0][i].size(); j++){
            QString value_name = QString(list_company[0][i][j]);
            value_name = value_name.mid(0, value_name.indexOf(": "));
//            qDebug() << "value_name: " << value_name << " index colum: " << list_colum_table.indexOf(value_name);
            //set cell if we have value of db
            if(list_colum_table.indexOf(value_name) != - 1){
                QString value = QString(list_company[0][i][j]);
                value = value.mid(value.indexOf(": ")+2);
                if(value == "None")
                    value = "";

                QTableWidgetItem *cell = new QTableWidgetItem();
                //we don't want user can change value of cell in table
                cell->setFlags(Qt::ItemIsSelectable|Qt::ItemIsUserCheckable|Qt::ItemIsEnabled);
                cell->setText(QApplication::translate("MainWindow", value.toLatin1(), 0));
                tableWidget->setItem(i, list_colum_table.indexOf(value_name), cell);
            }
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
