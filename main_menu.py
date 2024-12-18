
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import sys

class Ui_MainWindow(object):
    
    def __init__(self):
         self.MainWindow = None
         self.total_comboBox_list = []
         self.selected_tissues = []
         self.window_witdh = 653
         self.window_height = 398
         self.comboBox_offset = 80

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")

        self.MainWindow.resize(self.window_witdh, self.window_height)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 280, 231, 61))
        self.pushButton.setStyleSheet(
                "QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}"
        )
        self.pushButton.setObjectName("pushButton")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(40, 190, 571, 51))
        self.comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.comboBox.setObjectName("comboBox")
        self.total_comboBox_list.append(self.comboBox)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 125, 241, 61))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(340, 280, 231, 61))
        self.pushButton_2.setStyleSheet(
               "QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}"
        )
        self.pushButton_2.setObjectName("pushButton_2")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.add_combo_box)
        self.pushButton_2.clicked.connect(self.connect_push2)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "Add Tissue"))

        total_list = pd.read_csv("database/metadata_FACS.csv")["tissue"].unique()

        self.comboBox.clear()
        for tissue in total_list:
                self.comboBox.addItem(_translate("MainWindow", tissue))

        self.label.setText(_translate("MainWindow", "Tissue type:"))
        self.pushButton_2.setText(_translate("MainWindow", "Analyze"))

    def add_combo_box(self):
        self.window_height += self.comboBox_offset
        self.MainWindow.resize(self.window_witdh, self.window_height)

        x_push_1 = self.pushButton.geometry().x()
        y_push_1 = self.pushButton.geometry().y()

        x_push_2 = self.pushButton_2.geometry().x()
        y_push_2 = self.pushButton_2.geometry().y()

        self.pushButton.move(x_push_1, y_push_1 + self.comboBox_offset)
        self.pushButton_2.move(x_push_2, y_push_2 + self.comboBox_offset)

        last_comboBox_y = self.total_comboBox_list[-1].geometry().y()

        new_comboBox = QtWidgets.QComboBox(self.centralwidget)
        new_comboBox.setGeometry(QtCore.QRect(40, last_comboBox_y + self.comboBox_offset, 571, 51))
        new_comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        new_comboBox.setObjectName(f"comboBox{len(self.total_comboBox_list) + 1}")

        total_list = pd.read_csv("database/metadata_FACS.csv")["tissue"].unique()
        for tissue in total_list:
                new_comboBox.addItem(tissue)

        self.total_comboBox_list.append(new_comboBox)
        new_comboBox.show()
        
    def connect_push2(self):
        for combo in self.total_comboBox_list:
             self.selected_tissues.append(combo.currentText())
        self.total_comboBox_list = []
        self.MainWindow.close()

    def get_selected(self):
         return self.selected_tissues


def set_up(app):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_selected()
