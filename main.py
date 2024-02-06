import os
import sys

import requests
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]
x, y = map(float, '131.888700, 43.125505'.split(', '))
scale = 15
view = 'map'
k = 0.001
metka = False
x_metka = 0
y_metka = 0


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.point_lon, self.point_lat, full_address = self.get_lonlat(
            'Владивосток')
        self.btn_plus.clicked.connect(self.plus)
        self.btn_minus.clicked.connect(self.minus)
        self.search_btn.clicked.connect(self.search)
        self.btn_scheme.clicked.connect(self.change_view)
        self.btn_satellite.clicked.connect(self.change_view)
        self.btn_hybrid.clicked.connect(self.change_view)
        self.getImage()
        self.initUI()

    def getImage(self):
        if metka:
            map_request = f'https://static-maps.yandex.ru/1.x/?ll={x},{y}&z={scale}&l={view}&pt={x_metka},{y_metka},pm2rdm'
        else:
            map_request = f'https://static-maps.yandex.ru/1.x/?ll={x},{y}&z={scale}&l={view}'
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, 600, 550)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)

        self.image.move(0, 100)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def plus(self):
        global scale
        if scale != 21:
            scale += 1
            self.getImage()

            self.pixmap = QPixmap(self.map_file)

            self.image.setPixmap(self.pixmap)

    def minus(self):
        global scale
        if scale != 1:
            scale -= 1
            self.getImage()

            self.pixmap = QPixmap(self.map_file)

            self.image.setPixmap(self.pixmap)

    def search(self):
        global x, y, scale, x_metka, y_metka, metka
        search_text = self.lineEdit.text().lower()
        try:
            lon, lat, full_address = self.get_lonlat(search_text)
            self.set_full_address(full_address)
            self.search_text = search_text
            x = lon
            y = lat
            metka = True
            x_metka = lon
            y_metka = lat
            self.point_lon = lon
            self.point_lat = lat
            scale = 15
            self.getImage(True)
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        except Exception:
            # по запросу ничего не нашлось
            pass
        pass

    def get_lonlat(self, search):
        geocoder_apikey = '06e2c22e-3e27-43ce-8225-d618104b8f10'
        geocoder_request = f'https://geocode-maps.yandex.ru/1.x?geocode={search}&apikey={geocoder_apikey}&format=json'
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']

            pos = toponym['Point']['pos']
            lon, lat = [float(el) for el in pos.split()]
            full_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
            return lon, lat, full_address

    def set_full_address(self, full_address):
        pass

    def keyPressEvent(self, event):
        global x, y
        if event.key() == Qt.Key_PageUp:  # Код клавиши PgUp
            self.plus()
        elif event.key() == Qt.Key_PageDown:  # Код клавиши PgDown
            self.minus()
        elif event.key() == Qt.Key_W:
            y += k
        elif event.key() == Qt.Key_A:
            x -= k
        elif event.key() == Qt.Key_D:
            x += k
        elif event.key() == Qt.Key_S:
            y -= k
        elif event.key() == Qt.Key_Return:
            if self.lineEdit.text().lower():
                self.search()
        if event.key() in [Qt.Key_W, Qt.Key_S, Qt.Key_D, Qt.Key_A]:
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def change_view(self):
        global view
        button = self.sender()
        if button == self.btn_scheme:
            view = 'map'
        elif button == self.btn_satellite:
            view = 'sat'
        elif button == self.btn_hybrid:
            view = 'sat,skl'
        self.getImage()

        self.pixmap = QPixmap(self.map_file)

        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
