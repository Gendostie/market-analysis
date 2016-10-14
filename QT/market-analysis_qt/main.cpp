#include <QApplication>
#include "mainwindow.h"

//#include <QScrollArea>
//#include <QHBoxLayout>
//#include <QVBoxLayout>
//#include <QPushButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow w;
    w.setMinimumSize(w.size());
    w.setMaximumSize(w.size());
    w.showNormal();
    return app.exec();
}
