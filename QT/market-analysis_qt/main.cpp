#include <QApplication>
#include <QtDebug>

#include "mainwindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow w;
//    qDebug("Size windows: %d x %d", w.size().width(), w.size().height());
    w.setMinimumSize(w.size());
    w.setMaximumSize(w.size());
//    w.showNormal();

    return app.exec();
}
