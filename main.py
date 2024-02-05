import os
import sys

import requests
from PyQt5 import uic, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]
x, y = map(float, '43.125505, 131.888700'.split(', '))
scale = 15
view = 'map'
k = 0.001


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)

        self.btn_plus.clicked.connect(self.plus)
        self.btn_minus.clicked.connect(self.minus)
        self.btn_scheme.clicked.connect(self.change_view)
        self.btn_satellite.clicked.connect(self.change_view)
        self.btn_hybrid.clicked.connect(self.change_view)
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={y},{x}&z={scale}&l={view}"
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

    def keyPressEvent(self, event):
        global x, y
        if event.key() == Qt.Key_PageUp:  # Код клавиши PgUp
            self.plus()
        elif event.key() == Qt.Key_PageDown:  # Код клавиши PgDown
            self.minus()
        elif event.key() == Qt.Key_W:
            x += k
        elif event.key() == Qt.Key_A:
            y -= k
        elif event.key() == Qt.Key_D:
            y += k
        elif event.key() == Qt.Key_S:
            x -= k
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