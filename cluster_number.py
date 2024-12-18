
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.numberOfCluster = None


    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow 

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(526, 255)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 140, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(70, 30, 281, 61))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(310, 40, 141, 51))
        self.spinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1, 100)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.set_cluster_number)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "Do Clustering"))
        self.label.setText(_translate("MainWindow", "Number of Clusters"))

    def get_cluster_number(self):
        return self.numberOfCluster
    
    def set_cluster_number(self):
        self.numberOfCluster = self.spinBox.value()
        self.MainWindow.close()



def main(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_cluster_number()