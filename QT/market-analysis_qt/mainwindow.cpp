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

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    create_data_table_stock_screener(ui->tableWidget_stockScreener);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void create_data_table_stock_screener(QTableWidget *tableWidget){
    int nb_row_init = 13;

    //TODO: change for call sql
    QList<QStringList> *list_company = new QList<QStringList>;
    QStringList *l = new QStringList;
    l << "GOOGLE" << "GOOGL" << "1231" << "1231" << "1231" << "1231";
    l << "1231" << "1231" << "1231" << "1231" << "1231" << "1231" << "1231";
    list_company->append(l);

    if (tableWidget->rowCount() < nb_row_init)
            tableWidget->setRowCount(nb_row_init);

    const bool sorting_enabled = tableWidget->isSortingEnabled();
    tableWidget->setSortingEnabled(false);
    int i = 0;
    QString company;
    foreach (company, list_company) {
        //create new row
        QTableWidgetItem *cell = new QTableWidgetItem();
        tableWidget->setVerticalHeaderItem(i, cell);

        int j = 0;
        QString value;
        foreach (value, company) {
            //is last column, for checkbox
            if(j < tableWidget->columnCount() - 1){
                Q_ASSERT_X(j == 13, "create_data_table_stock_screener",
                           QString("The index of column is more than 13, i = %1").arg(i));

                QWidget * widget_cb = new QWidget();
                QHBoxLayout *hBoxLayout_cb = new QHBoxLayout();
                QCheckBox *cb = new QCheckBox();
                hBoxLayout_cb->setMargin(1);
                hBoxLayout_cb->setAlignment(Qt::AlignCenter);
                hBoxLayout_cb->addWidget(cb);
                widget_cb->setLayout(hBoxLayout_cb);
                ui->tableWidget_stockScreener->setCellWidget(i, j, widget_cb);
            }
            else{
                QTableWidgetItem *cell = new QTableWidgetItem();
                //we don't want user can change value of cell in table
                cell->setFlags(Qt::ItemIsSelectable|Qt::ItemIsUserCheckable|Qt::ItemIsEnabled);
                cell->setText(QApplication::translate("MainWindow", value, 0);
                tableWidget->setItem(i, j, cell);
            }
            j += 1;
        }
        i += 1;
    }
    tableWidget->setSortingEnabled(sorting_enabled);
}

//void /*QWidget*/ create_criteria(QString name_criteria, qint32 min_value, qint32 max_value, QString name_tag){
//    QWidget *horizontalLayoutWidget = new QWidget(frame);
//    horizontalLayoutWidget->setObjectName(QStringLiteral("hlw_" + name_tag));
//    horizontalLayoutWidget->setGeometry(QRect());

//    QHBoxLayout *horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
//    horizontalLayout.setObjectName(QStringLiteral("hbl_criteria_" + name_tag));
//    horizontalLayout->setContentsMargins(0, 0, 0, 0);

//    QCheckBox cb_criteria = new QCheckBox();
//    cb_criteria.setObjectName(QStringLiteral("cb_criteria_" + name_tag));
//    frame.addWidget(cb_criteria);
     //spacer = new QSpacerItem();


//    horizontalLayoutWidget_2 = new QWidget(frame);
//    horizontalLayoutWidget_2->setObjectName(QStringLiteral("horizontalLayoutWidget_2"));
//    horizontalLayoutWidget_2->setGeometry(QRect(10, 10, 1311, 181));
//    horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
//    horizontalLayout_2->setSpacing(6);
//    horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
//    horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
//    horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
//    verticalLayout = new QVBoxLayout();
//    verticalLayout->setSpacing(6);
//    verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
//    horizontalLayout_13 = new QHBoxLayout();
//    horizontalLayout_13->setSpacing(6);
//    horizontalLayout_13->setObjectName(QStringLiteral("horizontalLayout_13"));
//    horizontalLayout_13->setSizeConstraint(QLayout::SetDefaultConstraint);
//    checkBox_12 = new QCheckBox(horizontalLayoutWidget_2);
//    checkBox_12->setObjectName(QStringLiteral("checkBox_12"));
//    checkBox_12->setMinimumSize(QSize(150, 16));
//    checkBox_12->setMaximumSize(QSize(200, 16777215));

//    horizontalLayout_13->addWidget(checkBox_12);

//    horizontalSpacer_13 = new QSpacerItem(20, 20, QSizePolicy::Maximum, QSizePolicy::Minimum);

//    horizontalLayout_13->addItem(horizontalSpacer_13);

//    label_2 = new QLabel(horizontalLayoutWidget_2);
//    label_2->setObjectName(QStringLiteral("label_2"));
//    label_2->setMinimumSize(QSize(20, 0));
//    label_2->setMaximumSize(QSize(25, 16777215));

//    horizontalLayout_13->addWidget(label_2);

//    lineEdit = new QLineEdit(horizontalLayoutWidget_2);
//    lineEdit->setObjectName(QStringLiteral("lineEdit"));
//    lineEdit->setMinimumSize(QSize(40, 20));
//    lineEdit->setMaximumSize(QSize(30, 16777215));

//    horizontalLayout_13->addWidget(lineEdit);

//    horizontalSpacer = new QSpacerItem(20, 20, QSizePolicy::Fixed, QSizePolicy::Minimum);

//    horizontalLayout_13->addItem(horizontalSpacer);

//    label = new QLabel(horizontalLayoutWidget_2);
//    label->setObjectName(QStringLiteral("label"));
//    label->setMinimumSize(QSize(25, 0));
//    label->setMaximumSize(QSize(30, 16777215));

//    horizontalLayout_13->addWidget(label);

//    lineEdit_2 = new QLineEdit(horizontalLayoutWidget_2);
//    lineEdit_2->setObjectName(QStringLiteral("lineEdit_2"));
//    lineEdit_2->setMinimumSize(QSize(40, 20));
//    lineEdit_2->setMaximumSize(QSize(30, 16777215));

//    horizontalLayout_13->addWidget(lineEdit_2);


//    verticalLayout->addLayout(horizontalLayout_13);

//}
