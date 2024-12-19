from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import scprep


class Ui_MainWindow(object):
    def __init__(self, data, metadata, path):
        self.data = data
        self.metadata = metadata
        self.path = path

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(980, 864)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 740, 231, 61))
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
        self.label.setGeometry(QtCore.QRect(230, 630, 231, 61))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 740, 231, 61))
        self.pushButton_2.setStyleSheet("QPushButton {"
                "    background-color: rgb(169, 169, 253);"
                "    color: rgb(0, 0, 0);"
                "}"
                "QPushButton:hover {"
                "    background-color: rgb(134, 67, 0);"
                "    color: rgb(255, 255, 255);"
                "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(410, 640, 351, 51))
        self.comboBox.setStyleSheet("background-color: rgb(243, 238, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(self.metadata.columns)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.pushButton.clicked.connect(self.see_graph)
        self.pushButton_2.clicked.connect(self.next_step)
        

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "BioE c249 Final Project"))
        self.pushButton.setText(_translate("MainWindow", "See on graph"))
        self.label.setText(_translate("MainWindow", "Coloring Criteria: "))
        self.pushButton_2.setText(_translate("MainWindow", "Continue"))
        self.see_graph()
     
    def see_graph(self):
        criteria = self.comboBox.currentText()
        fig, axes = plt.subplots(2,3, figsize=(22, 8))

        axes = axes.flatten()
        for i, ax in enumerate(axes):
            legend = True if i == 2 else False
            scprep.plot.scatter(
                self.data.iloc[:, i],
                self.data.iloc[:, i + 1],
                c=self.metadata[criteria],
                cmap='Spectral',
                ax=ax,
                xlabel="PC_" + str(i + 1),
                ylabel="PC_" + str(i + 2),
                legend=legend,
                legend_loc="upper left",  
                legend_anchor=(1.05, 1),  
                filename=self.path + f"/scatter_PCA/scatter_plot_{criteria}.png"
            )

        fig.tight_layout(rect=[0, 0, 0.95, 1])
        pixmap = QPixmap(self.path+f"/scatter_PCA/scatter_plot_{criteria}.png")
        plt.close(fig)
        original_width = pixmap.width()
        original_height = pixmap.height()

        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(30, 10, 
                                                  original_width-int((460*(original_width/original_height))), 
                                                  original_height-int((580*(original_height/original_width)))))
        self.image_label.setScaledContents(True)
        
        self.image_label.setPixmap(pixmap)
        self.image_label.show()

    def next_step(self):
        self.MainWindow.close()
        

def main(app, data, metadata, path):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(data, metadata, path)
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
