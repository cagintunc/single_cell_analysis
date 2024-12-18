
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    
    def __init__(self):
        self.total_list = ['ward', 'complete', 'average', 'single']
        self.cluster_number, self.linkage = None, None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(819, 367)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 260, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(80, 40, 231, 61))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(360, 50, 141, 51))
        self.spinBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 140, 161, 61))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(360, 140, 441, 51))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.comboBox.addItems(self.total_list)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.pushButton.clicked.connect(self.set_parameters)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Agglomerative Clustering"))
        self.pushButton.setText(_translate("MainWindow", "Do Clustering"))
        self.label.setText(_translate("MainWindow", "Number of Clusters:"))
        self.label_2.setText(_translate("MainWindow", "Linkage:"))

    def set_parameters(self):
        self.cluster_number = self.spinBox.value()
        self.linkage = self.comboBox.currentText()
        self.MainWindow.close()

    def get_parameters(self):
        return self.cluster_number, self.linkage


def main(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_parameters()
    
