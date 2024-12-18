
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def __init__(self):
        self.eps = None
        self.minSample = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(526, 347)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 250, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(120, 30, 211, 61))
        self.label.setObjectName("label")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(300, 30, 131, 61))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.doubleSpinBox.setSingleStep(0.01)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 130, 211, 61))
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(300, 130, 131, 61))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox.setMinimum(1)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.set_parameters)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "Do DBSCAN"))
        self.label.setText(_translate("MainWindow", "Epsilon: "))
        self.label_2.setText(_translate("MainWindow", "Min Samples:"))


    def set_parameters(self):
        self.eps = self.doubleSpinBox.value()
        self.minSample = self.spinBox.value()
        self.MainWindow.close()

    def get_parameters(self):
        return self.eps, self.minSample



def main(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_parameters()
