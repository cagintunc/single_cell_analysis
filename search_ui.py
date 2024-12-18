

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.text = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(606, 239)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 120, 180, 61))
        self.pushButton.setStyleSheet("QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 571, 61))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 125, 371, 51))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                        "    background-color: rgb(250, 250, 250);\n"
                                        "    \n"
                                        "}")
        self.lineEdit.setObjectName("lineEdit")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.set_search)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Gene Search"))
        self.pushButton.setText(_translate("MainWindow", "Search"))
        self.label.setText(_translate("MainWindow", "Search a specific gene(s) by ID(s) (e.g. Zzef1, Zzz3,..):"))

    def set_search(self):
        self.text = self.lineEdit.text()
        self.MainWindow.close()

    def get_text(self):
        return self.text
        

def main(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_text()

