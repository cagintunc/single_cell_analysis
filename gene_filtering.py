
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtGui import QPixmap
import scprep
import matplotlib.pyplot as plt

class PowerOfTenSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(1, 4)  # Exponent range: 10^1 to 10^4
        self.setSingleStep(1)  # Increment by powers of 10

    def textFromValue(self, value):
        # Display the value as 10^x
        return f"10^{value}"

    def valueFromText(self, text):
        if text.startswith("10^"):
            try:
                return int(text.value()[3:])  
            except ValueError:
                pass
        return 1  

    def stepBy(self, steps):
        new_value = self.value() + steps
        if self.minimum() <= new_value <= self.maximum():
            self.setValue(new_value)

    def get_real_value(self):
        return 10 ** self.value()

class Ui_MainWindow(object):
    def __init__(self, data, path):
        self.data = data
        self.experiment_path = path
        self.cutoff = None

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(667, 704)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 580, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(150, 470, 231, 61))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 580, 231, 61))
        self.pushButton_2.setStyleSheet("QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.spinBox = PowerOfTenSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(360, 480, 141, 51))
        self.spinBox.setStyleSheet("background-color: rgb(110, 65, 97);\n"
                                        "color: rgb(255, 255, 255);")
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setSingleStep(10)
        self.spinBox.setRange(0, 100)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(37, 10, 590, 420))
        self.image_label.setScaledContents(True)  # Ensure the image fits the label
        pixmap = QPixmap(self.experiment_path+"/before_cutoff.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.show()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.see_graph)
        self.pushButton_2.clicked.connect(self.set_cutoff)
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "See on graph"))
        self.label.setText(_translate("MainWindow", "Cutoff value:"))
        self.pushButton_2.setText(_translate("MainWindow", "Filter"))

    def see_graph(self):
        fig, ax = plt.subplots()
        scprep.plot.histogram(scprep.measure.gene_capture_count(self.data), log=True,
                                cutoff=self.spinBox.get_real_value(),
                                title="Gene Captured",
                                xlabel='# of cells with nonzero expression',
                                ylabel='# of genes',
                                ax=ax,
                                filename=self.experiment_path+"/before_cutoff.png")
        plt.close(fig)

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(37, 10, 590, 420))
        self.image_label.setScaledContents(True)  # Ensure the image fits the label

        pixmap = QPixmap(self.experiment_path+"/before_cutoff.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.show()

    def set_cutoff(self):
        self.cutoff = self.spinBox.get_real_value()
        self.MainWindow.close()

    def get_cutoff(self):
        return self.cutoff


def main(app, data, path):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(data, path)
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    return ui.get_cutoff()
