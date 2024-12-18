

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.selected = None

    def setupUi(self, MainWindow, array):
        self.array = array
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(653, 398)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 210, 571, 41))
        self.comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 120, 441, 61))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 290, 231, 61))
        self.pushButton_2.setStyleSheet("QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.pushButton_2.clicked.connect(self.set_cluster_selection)    


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.comboBox.addItems(self.array)
        self.label.setText(_translate("MainWindow", "Select the clustering algorithm:"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))

    def set_cluster_selection(self):
        self.selected = self.comboBox.currentText()
        self.MainWindow.close()

    def get_cluster_selection(self):
        return self.selected


def main(app, c):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, c)
    MainWindow.show()
    app.exec_()
    return ui.get_cluster_selection()
