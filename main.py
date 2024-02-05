import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]
x, y = map(float, '43.125505, 131.888700'.split(', '))
scale = 1


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)

        self.pushButton.clicked.connect(self.plus)
        self.pushButton_2.clicked.connect(self.minus)
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={y},{x}&z={scale}&l=map"
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

    def closeEvent(self, event):
        os.remove(self.map_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())