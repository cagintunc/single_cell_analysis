
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    
    def __init__(self):
        self.pca_number = 0
    
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
        self.pushButton.setGeometry(QtCore.QRect(140, 150, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(90, 50, 231, 61))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(290, 60, 141, 51))
        self.spinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox.setMinimum(7)
        self.spinBox.setObjectName("spinBox")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.pca_push)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Do PCA Analysis"))
        self.label.setText(_translate("MainWindow", "Number of PCs:"))
    
    def pca_push(self):
        self.pca_number = self.spinBox.value()
        self.MainWindow.close()

    def get_pca(self):
        return self.pca_number


def main(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_pca()

