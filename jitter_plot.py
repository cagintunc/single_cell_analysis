
from PyQt5 import QtCore, QtGui, QtWidgets
import scprep
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap

class Ui_MainWindow(object):

    def __init__(self):
        self.filter = None
        self.image_label = None
        self.pushButton_2 = None

    def setupUi(self, MainWindow, genes, data, clusters, experiment_path):
        self.data = data
        self.genes = genes
        self.clusters = clusters
        self.MainWindow = MainWindow
        self.experiment_path = experiment_path

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(769, 295)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(270, 180, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(170, 30, 151, 61))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(250, 40, 441, 51))
        self.comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(genes)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.pushButton.clicked.connect(self.show_jitter_plot)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Gene Analysis"))
        self.pushButton.setText(_translate("MainWindow", "Plot"))
        self.label.setText(_translate("MainWindow", "Genes"))
    
    def show_jitter_plot(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.resize(697, 700)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 600, 231, 61))
        self.pushButton_2.setStyleSheet("QPushButton {"
                                        "    background-color: rgb(169, 169, 253);"
                                        "    color: rgb(0, 0, 0);"
                                        "}"
                                        "QPushButton:hover {"
                                        "    background-color: rgb(134, 67, 0);"
                                        "    color: rgb(255, 255, 255);"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText(_translate("MainWindow", "Continue"))
        self.pushButton_2.show()  

        self.pushButton_2.clicked.connect(self.next_step)

        self.pushButton.setGeometry(QtCore.QRect(70, 600, 231, 61))
        self.label.setGeometry(QtCore.QRect(70, 460, 151, 61))
        self.comboBox.setGeometry(QtCore.QRect(160, 470, 441, 51))

        current_filter = self.comboBox.currentText()
        curr_expression = scprep.select.select_cols(self.data, exact_word=current_filter)
        fig, ax = plt.subplots()
        scprep.plot.jitter(self.clusters, curr_expression, c=self.clusters, figsize=(12, 5),
                            legend_anchor=(1,1), title=current_filter, ax=ax,
                            filename=self.experiment_path+f"/jitter_{current_filter}.png")
        plt.close(fig)

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(37, 10, 590, 420))
        self.image_label.setScaledContents(True) 

        pixmap = QPixmap(self.experiment_path+f"/jitter_{current_filter}.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.show()

    def next_step(self):
        self.MainWindow.close()
    

def main(app, genes, data, clusters, path):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, genes, data, clusters, path)
    MainWindow.show()
    app.exec_()
