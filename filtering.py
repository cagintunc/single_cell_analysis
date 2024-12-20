
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import scprep
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap

class Ui_MainWindow(object):
    
    def __init__(self, data, path):
        self.show_graph = False
        self.data = data
        self.experiment_path = path
        self.image_label = None
        self.percentile = None

    def setupUi(self, MainWindow):
        self.MainMenu = MainWindow
        self.MainMenu.setObjectName("MainWindow")

        self.MainMenu.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
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
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setStyleSheet("QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setSingleStep(5)
        self.spinBox.setRange(0, 100)

        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setSingleStep(5)
        self.spinBox_2.setRange(0, 100)

        self.MainMenu.resize(667, 398)
        self.pushButton.setGeometry(QtCore.QRect(80, 280, 231, 61))
        self.label.setGeometry(QtCore.QRect(100, 80, 291, 61))
        self.pushButton_2.setGeometry(QtCore.QRect(340, 280, 231, 61))
        self.label_2.setGeometry(QtCore.QRect(100, 160, 301, 61))
        self.spinBox.setGeometry(QtCore.QRect(400, 90, 161, 51))
        self.spinBox_2.setGeometry(QtCore.QRect(400, 160, 161, 51))

        self.MainMenu.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainMenu)
        self.statusbar.setObjectName("statusbar")
        self.MainMenu.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainMenu)

        #for constraints
        self.spinBox.valueChanged.connect(self.update_constraints)
        self.spinBox_2.valueChanged.connect(self.update_constraints)

        #now real buttons
        self.pushButton.clicked.connect(self.see_graph)
        self.pushButton_2.clicked.connect(self.next_process)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainMenu.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "See on graph"))
        self.label.setText(_translate("MainWindow", "Lower percentile:"))
        self.pushButton_2.setText(_translate("MainWindow", "Filter"))
        self.label_2.setText(_translate("MainWindow", "Higher percentile:"))

    #Function to ensure the constraints are satisfied: high>low should be hold.
    def update_constraints(self):
        if self.spinBox.value() > self.spinBox_2.value():
            temp_value = self.spinBox_2.value()
            self.spinBox_2.setValue(self.spinBox.value())
            self.spinBox.setValue(temp_value)

    def see_graph(self):
        low = self.spinBox.value()
        high = self.spinBox_2.value()
        self.percentile = (low, high)

        self.MainMenu.resize(667, 700)
        self.pushButton.setGeometry(QtCore.QRect(80, 600, 231, 61))
        self.label.setGeometry(QtCore.QRect(120, 460, 291, 61))
        self.pushButton_2.setGeometry(QtCore.QRect(340, 600, 231, 61))
        self.label_2.setGeometry(QtCore.QRect(120, 520, 301, 61))
        self.spinBox.setGeometry(QtCore.QRect(380, 470, 161, 45))
        self.spinBox_2.setGeometry(QtCore.QRect(380, 530, 161, 45))

        fig, ax = plt.subplots()
        scprep.plot.plot_library_size(
                data=self.data,
                title="Library size before filtering",
                ax=ax,  # Pass the custom axis to suppress `show()`
                filename=self.experiment_path+"/temporary_image.png",
                percentile=self.percentile
        )
        plt.close(fig)

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(37, 10, 590, 420))
        self.image_label.setScaledContents(True)  # Ensure the image fits the label

        pixmap = QPixmap(self.experiment_path+"/temporary_image.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.show()
    
    def get_final_percentiles(self):
        return self.percentile
    
    def next_process(self):
        low = self.spinBox.value()
        high = self.spinBox_2.value()
        self.percentile = (low, high)
        
        self.MainMenu.close()
          


def main(app, data, path):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(data, path)
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_final_percentiles()

