from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import io
import requests
from PyQt5.QtCore import Qt
import math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


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
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 361, 41))
        self.label_3.setFont(font)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(380, 90, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)

        self.MapType = 'map'
        self.spn = '0.005,0.005'

        self.retranslateUi()
        self.pts = []

    def retranslateUi(self):
        self.search_btn.setText("Search")
        self.pushButton_2.setText("Reset")
        self.checkBox.setText("PostIndex")
        self.search_btn.clicked.connect(self.search)
        self.comboBox.activated[str].connect(self.onChanged)
        self.checkBox.stateChanged.connect(self.show_postalcode)
        self.pushButton_2.clicked.connect(self.reset)

    def onChanged(self, text):
        if text == 'Спутник':
            self.MapType = 'sat'
        elif text == 'Гибрид':
            self.MapType = 'sat,skl'
        elif text == 'Схема':
            self.MapType = 'map'
        self.comboBox.clearFocus()

    def search(self):
        try:
            if self.lineEdit_2.text() != '':
                self.spn = self.lineEdit_2.text()
            response = requests.request(method='GET',
                                        url='http://static-maps.yandex.ru/1.x',
                                        params={
                                            'l': self.MapType,
                                            'll': self.lineEdit.text(),
                                            'spn': self.spn})
            data = io.BytesIO(response.content).getvalue()
            self.map_image = QtGui.QPixmap()
            self.map_image.loadFromData(data)
            self.label.setPixmap(self.map_image)
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
            self.show()
            self.current_cords = list(map(float, self.lineEdit.text().split(',')))
        except:
            print('ERROR')
        self.search_btn.clearFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            temp = self.spn.split(',')
            if float(temp[0]) < 75 and float(temp[1]) < 75:
                self.spn = str(round(float(temp[0]) + float(temp[0]) / 5, 6)) + ',' + str(
                    round(float(temp[1]) + float(temp[1]) / 5, 6))
                self.search()
        elif event.key() == Qt.Key_PageDown:
            temp = self.spn.split(',')
            self.spn = str(round(float(temp[0]) - float(temp[0]) / 5, 6)) + ',' + str(
                round(float(temp[1]) - float(temp[1]) / 5, 6))
            self.search()
        elif event.key() == Qt.Key_Right:
            temp = list(map(float, self.spn.split(',')))
            self.current_cords[0] += temp[0]
            self.lineEdit.setText(str(self.current_cords[0]) + ',' + str(self.current_cords[1]))
            self.search()
        elif event.key() == Qt.Key_Left:
            temp = list(map(float, self.spn.split(',')))
            self.current_cords[0] -= temp[0]
            self.lineEdit.setText(str(self.current_cords[0]) + ',' + str(self.current_cords[1]))
            self.search()
        elif event.key() == Qt.Key_Up:
            temp = list(map(float, self.spn.split(',')))
            self.current_cords[1] += temp[1]
            self.lineEdit.setText(str(self.current_cords[0]) + ',' + str(self.current_cords[1]))
            self.search()
        elif event.key() == Qt.Key_Down:
            temp = list(map(float, self.spn.split(',')))
            self.current_cords[1] -= temp[1]
            self.lineEdit.setText(str(self.current_cords[0]) + ',' + str(self.current_cords[1]))
            self.search()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.y() > 150:
                dx = 300 - event.x()
                dy = 375 - event.y()
                pos = list(map(float, self.lineEdit.text().split(',')))
                spn = list(map(float, self.spn.split(',')))
                x = pos[0] - dx * spn[0] * 0.00558493151
                y = pos[1] + dy * spn[1] * 0.00224583333
                geocoder_request = requests.request(method='GET',
                                                    url='http://geocode-maps.yandex.ru/1.x',
                                                    params={
                                                        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                                        'geocode': f'{x},{y}',
                                                        'format': 'json'})
                json_response = geocoder_request.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                adress = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                self.label_2.setText(adress)
        elif event.button() == Qt.RightButton:
            if event.y() > 150:
                dx = 300 - event.x()
                dy = 375 - event.y()
                pos = list(map(float, self.lineEdit.text().split(',')))
                spn = list(map(float, self.spn.split(',')))
                x = pos[0] - dx * spn[0] * 0.00558493151
                y = pos[1] + dy * spn[1] * 0.00224583333
                apikey_organizations = "0c285c96-1fb6-4d68-be42-7a67e33e7652"
                response = requests.request(method='GET',
                                            url="https://search-maps.yandex.ru/v1/",
                                            params={
                                                'apikey': apikey_organizations,
                                                'lang': 'ru_RU',
                                                'll': f'{x},{y}',
                                                'type': 'biz',
                                                'text': f'аптека',
                                                'results': 1}
                                            )
                json_response = response.json()
                organization = json_response["features"][0]
                coords = organization["geometry"]["coordinates"]
                if lonlat_distance([x, y], coords) <= 50:
                    name = organization["properties"]["name"]
                    self.label_2.setText(name)
                else:
                    self.label_2.setText(f'Расстояние больше 50 метров({round(lonlat_distance([x, y], coords))})')


    def show_postalcode(self):
        try:
            if self.checkBox.isChecked():
                self.label_3.show()
                geocoder_request = requests.request(method='GET',
                                                    url='http://geocode-maps.yandex.ru/1.x',
                                                    params={
                                                        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                                        'geocode': self.lineEdit.text(),
                                                        'format': 'json'})
                json_response = geocoder_request.json()
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                postalcode = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                self.label_3.setText(postalcode)
            else:
                self.label_3.hide()
        except:
            print('ERROR')

    def reset(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.label_2.setText('')
        self.spn = '0.005,0.005'
        self.MapType = 'map'
        self.pushButton_2.clearFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
