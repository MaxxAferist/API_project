from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import io
import requests
from PyQt5.QtCore import Qt


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.spn = '0.005,0.005'
        super().__init__()
        self.resize(600, 600)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 150, 600, 450))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 361, 31))
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 361, 31))
        self.search_btn = QtWidgets.QPushButton(self)
        self.search_btn.setGeometry(QtCore.QRect(380, 10, 101, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.search_btn.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 40, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(490, 10, 101, 22))
        self.comboBox.addItem("Схема")
        self.comboBox.addItem("Спутник")
        self.comboBox.addItem("Гибрид")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(380, 90, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)

        self.retranslateUi()

    def retranslateUi(self):
        self.search_btn.setText("Search")
        self.pushButton_2.setText("Reset")
        self.checkBox.setText("PostIndex")
        self.search_btn.clicked.connect(self.search)

    def search(self):
        try:
            if self.lineEdit_2.text() != '':
                self.spn = self.lineEdit_2.text()
            print(self.lineEdit.text())
            response = requests.request(method='GET',
                                        url='http://static-maps.yandex.ru/1.x',
                                        params={
                                            'l': 'map',
                                            'll': self.lineEdit.text(),
                                            'spn': self.spn})
            data = io.BytesIO(response.content).getvalue()
            self.map_image = QtGui.QPixmap()
            self.map_image.loadFromData(data)
            self.label.setPixmap(self.map_image)
        except:
            print('ERROR')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            temp = self.spn.split(',')
            if float(temp[0]) < 75 and float(temp[1]) < 75:
                self.spn = str(float(temp[0]) + float(temp[0]) / 5) + ',' + str(float(temp[1]) + float(temp[1]) / 5)
                self.search()
        elif event.key() == Qt.Key_PageDown:
            temp = self.spn.split(',')
            self.spn = str(float(temp[0]) - float(temp[0]) / 5) + ',' + str(float(temp[1]) - float(temp[1]) / 5)
            print(self.spn)
            self.search()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
