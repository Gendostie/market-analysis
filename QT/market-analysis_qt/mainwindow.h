#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    void create_data_table_stock_screener(QTableWidget *tableWidget);

    QString call_function_python(QString name_folder_file_py, QString name_python_file, QString name_fct, QString args);
    QList<QStringList> format_result_to_python(QString result);
};

#endif // MAINWINDOW_H
