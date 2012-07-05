#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QProcess>
#include <QDir>
#include <QPalette>
#include <QtDebug>
#include <QDomDocument>
#include <QStandardItem>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QFile file("/workspace/project/gyagp/test/linux/command/command.xml");
    if(not file.open(QIODevice::ReadOnly)) {
        qDebug() << "Can't open the command.xml!" << endl;
        return;
    }

    model = new QStandardItemModel();
    model->setColumnCount(3);
    model->setHorizontalHeaderItem(0, new QStandardItem("cmd"));
    model->setHorizontalHeaderItem(1, new QStandardItem("desc"));
    model->setHorizontalHeaderItem(2, new QStandardItem("rank"));

    QDomDocument doc;
    doc.setContent(&file);
    file.close();

    QDomElement commands = doc.documentElement();
    QDomNode command = commands.firstChild();

    int command_index = 0;
    while (!command.isNull()) {
        QDomElement cmd = command.firstChildElement();
        model->setItem(command_index, 0, new QStandardItem(cmd.text()));

        QDomElement desc = cmd.nextSiblingElement();
        model->setItem(command_index, 1, new QStandardItem(desc.text()));

        QDomElement rank = desc.nextSiblingElement();
        model->setItem(command_index, 2, new QStandardItem(rank.text()));

        command_index++;
        command = command.nextSibling();
    }

    modelProxy = new QSortFilterProxyModel(this);
    modelProxy->setSourceModel(model);
    modelProxy->setFilterKeyColumn(0);
    ui->tableView->setModel(modelProxy);
    ui->tableView->resizeColumnsToContents();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    QProcess *proc = new QProcess;

    proc->start(ui->plainTextEdit_command->toPlainText());

    if (!proc->waitForStarted()) {
        ui->plainTextEdit_output->setPlainText("Wrong command!");
        return;
    }

    proc->waitForFinished();
    ui->plainTextEdit_output->setPlainText(proc->readAll());
}

void MainWindow::on_plainTextEdit_dir_updateRequest(const QRect &rect, int dy)
{
    Q_UNUSED(rect);
    Q_UNUSED(dy);

    QPalette p = ui->plainTextEdit_dir->palette();

    if (!QDir(ui->plainTextEdit_dir->toPlainText()).exists()) {
        p.setColor(QPalette::Text, Qt::red);
        ui->plainTextEdit_dir->setPalette(p);
    } else {
        p.setColor(QPalette::Text, Qt::black);
        ui->plainTextEdit_dir->setPalette(p);
        QDir::setCurrent(ui->plainTextEdit_dir->toPlainText());
    }
}

void MainWindow::on_pushButton_2_clicked()
{
    QRegExp::PatternSyntax syntax = QRegExp::PatternSyntax(0);
    QRegExp regExp(ui->lineEdit_filter->text(), Qt::CaseInsensitive, syntax);
    modelProxy->setFilterRegExp(regExp);
}
