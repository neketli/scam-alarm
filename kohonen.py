import sys
from minisom import MiniSom
import numpy as np
import matplotlib.pyplot as plt
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 300)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 60, 160, 25))
        self.lineEdit.setText("10000")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 200, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 200, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 120, 160, 25))
        self.lineEdit_2.setText("0.5")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 160, 200, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 180, 160, 25))
        self.lineEdit_3.setText("0.7")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 250, 100, 30))
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(240, 110, 121, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(240, 140, 121, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setGeometry(QtCore.QRect(240, 170, 150, 20))
        self.radioButton_3.setObjectName("radioButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Кластеризация SOM"))
        self.label.setText(_translate("Dialog", "Введите количество итераций"))
        self.label_2.setText(_translate("Dialog", "Введите скорость обучения (0,1)"))
        self.label_3.setText(_translate("Dialog", "Введите сигма (0,1)"))
        self.pushButton.setText(_translate("Dialog", "Готово"))
        self.radioButton.setText(_translate("Dialog", "Загрузить сеть"))
        self.radioButton_2.setText(_translate("Dialog", "Сохранить сеть"))
        self.radioButton_3.setText(_translate("Dialog", "Обучить и забыть"))


sys.path.insert(0, '../')

app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()


def button():
    data = np.genfromtxt('students_test.txt', delimiter=',')
    initialData = [str(i) for i in data]
    dataArr = data.tolist()

    if ui.radioButton.isChecked():
        with open('som.p', 'rb') as infile:
            som = pickle.load(infile)
        print("loaded successfully")

        # Номарнализация
        data = data - np.mean(data, axis=0)  # среднее арифм
        data /= np.std(data)  # стандартное отклонение

        winner_coordinates = np.array([som.winner(x) for x in data]).T
        dataClusters = winner_coordinates[1].tolist()

        with open(r"output.txt", "w") as file:  # вывод в файл с кластерами (можно и по именам)
            j = 0
            for i in range(len(winner_coordinates[1])):
                j += 1
                file.write(
                    'Student:' + str(j) + ' with points: ' + initialData[i] + ' was assigned to a cluster - ' + str(
                        dataClusters[i]+1) + '\n')

        arrPoints = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        counter = [0, 0, 0]

        for i in range(len(dataClusters)):
            if dataClusters[i] == 0:
                counter[0] += 1
                for k in range(3):
                    arrPoints[0][k] += dataArr[i][k]
            elif dataClusters[i] == 1:
                counter[1] += 1
                for k in range(3):
                    arrPoints[1][k] += dataArr[i][k]
            elif dataClusters[i] == 2:
                counter[2] += 1
                for k in range(3):
                    arrPoints[2][k] += dataArr[i][k]

        for i in range(3):
            for j in range(3):
                if counter[i] != 0:
                    arrPoints[i][j] = int(arrPoints[i][j] / counter[i])

        # с помощью np.ravel_multi_index мы конвертируем двумерные координаты к одномерному индексу
        cluster_index = np.ravel_multi_index(winner_coordinates, (1, 3))

        # построение кластеров с использованием первых двух измерений данных
        for c in np.unique(cluster_index):
            plt.scatter(data[cluster_index == c, 0],
                        data[cluster_index == c, 1],
                        label='Кластер №' + str(c + 1) + ', количество ученников ' + str(
                            counter[c]) + ', средний балл = ' + str(arrPoints[c]),
                        alpha=.7)

        for centroid in som.get_weights():
            plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
                        s=80, linewidths=35, color='k', label='Центр')

        plt.grid(color='gray', linewidth=0.2)
        plt.legend(title='Легенда', loc='best')
        plt.show()

    if ui.radioButton_2.isChecked() or ui.radioButton_3.isChecked():

        n = int(ui.lineEdit.text())
        k = float(ui.lineEdit_2.text())
        sigm = float(ui.lineEdit_3.text())

        # Номарнализация
        data = data - np.mean(data, axis=0)  # среднее арифм
        data /= np.std(data)  # стандартное отклонение

        # инициализация и тренировка
        som_shape = (1, 3)  # количество кластеров
        som = MiniSom(som_shape[0], som_shape[1], 3, sigma=sigm, learning_rate=k,
                      neighborhood_function='gaussian', random_seed=10)

        som.random_weights_init(data)  # Инициализируем веса для матрцы
        som.train(data, n, verbose=True)

        # каждый нейрон представляет собой кластер
        winner_coordinates = np.array([som.winner(x) for x in data]).T
        dataClusters = winner_coordinates[1].tolist()

        with open(r"output.txt", "w") as file:  # вывод в файл с кластерами (можно и по именам)
            j = 0
            for i in range(len(winner_coordinates[1])):
                j += 1
                file.write('Student:'+str(j)+' with points: '+initialData[i] +
                           ' was assigned to a cluster - '+str(dataClusters[i]+1)+'\n')

        arrPoints = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        counter = [0, 0, 0]

        for i in range(len(dataClusters)):
            if dataClusters[i] == 0:
                counter[0] += 1
                for k in range(3):
                    arrPoints[0][k] += dataArr[i][k]
            elif dataClusters[i] == 1:
                counter[1] += 1
                for k in range(3):
                    arrPoints[1][k] += dataArr[i][k]
            elif dataClusters[i] == 2:
                counter[2] += 1
                for k in range(3):
                    arrPoints[2][k] += dataArr[i][k]

        for i in range(3):
            for j in range(3):
                if counter[i] != 0:
                    arrPoints[i][j] = int(arrPoints[i][j]/counter[i])

        # с помощью np.ravel_multi_index мы конвертируем двумерные координаты к одномерному индексу
        cluster_index = np.ravel_multi_index(winner_coordinates, (1, 3))

        # построение кластеров с использованием первых двух измерений данных
        for c in np.unique(cluster_index):
            plt.scatter(data[cluster_index == c, 0],
                        data[cluster_index == c, 1],
                        label='Кластер №'+str(c+1)+', количество ученников ' +
                        str(counter[c])+', средний балл = '+str(arrPoints[c]), alpha=.7)

        # plotting centroids
        for centroid in som.get_weights():
            plt.scatter(centroid[:, 0], centroid[:, 1], marker='x',
                        s=80, linewidths=35, color='k', label='Центр')

        plt.grid(color='gray', linewidth=0.2)
        plt.legend(title='Легенда', loc='best')
        plt.show()

        if ui.radioButton_2.isChecked():
            with open('som.p', 'wb') as outfile:
                pickle.dump(som, outfile)
            print("saved successfully")

ui.pushButton.clicked.connect(button)
sys.exit(app.exec_())
