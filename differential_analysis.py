from PyQt5 import QtCore, QtGui, QtWidgets
import scprep
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, cluster_id, data_sparse, path, cluster):
        self.MainWindow = MainWindow
        self.cluster_id = cluster_id
        self.data_sparse = data_sparse
        self.path = path
        self.cluster = cluster

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(769, 333)
        self.MainWindow.setStyleSheet("background-color: rgb(222, 224, 255);\n"
                                "color: rgb(0, 0, 0);\n"
                                "font: 12pt \"Berlin Sans FB\";")
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 100, 231, 51))
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
        self.label.setGeometry(QtCore.QRect(95, 90, 131, 61))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(230, 100, 161, 51))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(self.cluster_id)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 20, 391, 61))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 160, 631, 431))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.pushButton.clicked.connect(self.get_statistics)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "See Results"))
        self.label.setText(_translate("MainWindow", "Cluster"))
        self.label_2.setText(_translate("MainWindow", "Differential Expression Statistics"))
        self.label_3.setText(_translate("MainWindow", ""))

    def get_statistics(self):
        curr_cluster = int(self.comboBox.currentText()) - 1
        if not os.path.exists(self.path+"/differential_statistics"):
            os.mkdir(self.path+"/differential_statistics")

        data_in_cluster = self.data_sparse[self.cluster == curr_cluster]
        data_out_cluster = self.data_sparse[self.cluster != curr_cluster]

        if data_in_cluster.shape[0] == 0 or data_out_cluster.shape[0] == 0:
            self.label_3.setText("Error: No data available for selected cluster.")
            return

        try:
            ttest_results = scprep.stats.differential_expression(
                data_in_cluster, data_out_cluster, measure='ttest'
            )
            ttest_results.to_csv(self.path + f"/differential_statistics/differential_expression_{curr_cluster}.csv")
            text = get_text(ttest_results)
            self.MainWindow.resize(769, 620)
            self.label_3.setTextFormat(QtCore.Qt.RichText)
            self.label_3.setText(text)
        except ZeroDivisionError:
            self.label_3.setText("Error: Division by zero in statistical calculations.")



def get_text(df):
    result = "<pre>"  
    result += "{:<20}{:>15}\n".format("Gene Name", "Test Score")
    result += "{:<20}{:>15}\n\n".format("---------", "----------")
    
    names = list(df.index)
    ttest = list(df["ttest"])
    for i in range(5):
        line = "{:<20}{:>15.3f}\n\n".format(names[i], ttest[i])
        result += line
    result += "</pre>"  
    return result



def main(app, cluster_ids, data_sparse, path, cluster):
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, cluster_ids, data_sparse, path, cluster)
    MainWindow.show()
    app.exec_()
