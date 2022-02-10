from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import io
import requests


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
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
        self.checkBox.setText("Address")
        self.search_btn.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.reset)
        self.checkBox.stateChanged.connect(self.show_address)

    def reset(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.label_2.setText('')

    def show_address(self):
        try:
            if self.checkBox.isChecked():
                self.label_2.show()
                geocoder_request = requests.request(method='GET',
                                                    url='http://geocode-maps.yandex.ru/1.x',
                                                    params={
                                                        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                                        'geocode': self.lineEdit.text(),
                                                        'format': 'json'})
                json_response = geocoder_request.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                adress = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                self.label_2.setText(adress)
            else:
                self.label_2.hide()
        except:
            print('ERROR')

    def search(self):
        try:
            spn = '0.005,0.005'
            if self.lineEdit_2.text() != '':
                spn = self.lineEdit_2.text()
            response = requests.request(method='GET',
                                        url='http://static-maps.yandex.ru/1.x',
                                        params={
                                            'l': 'map',
                                            'll': self.lineEdit.text(),
                                            'spn': spn})
            print(response.url)
            data = io.BytesIO(response.content).getvalue()
            self.map_image = QtGui.QPixmap()
            self.map_image.loadFromData(data)
            self.label.setPixmap(self.map_image)
            self.show_address()
            self.checkBox.setChecked(True)

        except:
            print('ERROR')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())