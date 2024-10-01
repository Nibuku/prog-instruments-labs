import os
import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import search_with_date
import separation_by_date_and_data
import separation_on_weeks
import separation_on_year


class Window(QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()

        self.setGeometry(300, 250, 1007, 925)
        self.setFixedSize(1007, 925)
        self.setWindowTitle("Погода")
        self.background = QLabel(self)
        self.fire = QLabel(self)
        # self.background = QPixmap('cat_with_lighting.jpeg')
        self.background.setGeometry(0, 0, 1007, 925)
        self.background.setPixmap(QPixmap("cat_with_lighting.jpeg"))

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Создание и выбор аннотаций")
        self.main_text.move(725, 10)
        self.main_text.adjustSize()

        self.folderpath_dataset = ""
        while self.folderpath_dataset == "":
            self.folderpath_dataset = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Please select folder of dataset"
            )

        self.botton1 = QtWidgets.QPushButton(self)
        self.botton1.setText("Разделение на года")
        self.botton1.setFixedWidth(300)
        self.botton1.move(670, 30)
        self.botton1.clicked.connect(self.cleek_year)

        self.botton2 = QtWidgets.QPushButton(self)
        self.botton2.setText("Разделение на недели")
        self.botton2.setFixedWidth(300)
        self.botton2.move(670, 60)
        self.botton2.clicked.connect(self.cleek_week)

        self.botton3 = QtWidgets.QPushButton(self)
        self.botton3.setText("Разделение на даты и данные")
        self.botton3.setFixedWidth(300)
        self.botton3.move(670, 90)
        self.botton3.clicked.connect(self.cleek_data_date)

        self.text = QtWidgets.QLabel(self)
        self.weather_text = QtWidgets.QLabel(self)
        self.btn_weather = QtWidgets.QPushButton(self)
        self.btn_weather.hide()
        self.btn_next = QtWidgets.QPushButton(self)
        self.btn_next.hide()
        self.dateEdit = QtWidgets.QDateEdit(self)
        self.dateEdit.hide()

    def hidden_text(self):
        self.text.setText("Введите дату дд/мм/гггг")
        self.text.move(735, 120)
        self.text.adjustSize()

        self.fire.setGeometry(0, 0, 686, 520)
        self.fire.setPixmap(QPixmap("pngwing.com.png"))
        self.fire.hide()

        # self.calendar.setText("hjh")
        self.dateEdit.show()
        self.dateEdit.move(760, 136)
        # self.dateEdit.setFixedWidth(200)

        self.weather_text.setText("Данные")
        self.weather_text.move(65, 310)
        self.weather_text.setFixedWidth(500)
        # self.weather_text.setFixedHeigth(100)
        self.weather_text.setStyleSheet("color: rgb(0, 0, 0); font-size: 16px;")
        self.weather_text.hide()

        self.btn_weather.show()
        self.btn_weather.setText("Получить данные")
        self.btn_weather.setFixedWidth(200)
        self.btn_weather.move(720, 170)
        self.btn_weather.clicked.connect(self.cleek_data_of_weather)

    def cleek_data_date(self) -> None:
        separation_by_date_and_data.main()
        self.flag = 1
        self.hidden_text()

    def cleek_week(self) -> None:
        separation_on_weeks.main()
        self.flag = 2
        self.hidden_text()

    def cleek_year(self) -> None:
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Save dataset by years", "", ";All Files (*)")
        if not os.path.isdir(fname[0]):
            os.mkdir(fname[0])
        separation_on_year.separetion_year(fname[0])
        self.flag = 3
        self.hidden_text()

    def cleek_data_of_weather(self) -> None:
        text = ""
        self.fire.show()
        self.weather_text.show()
        if self.flag == 1:
            text = search_with_date.search_in_data_and_date(
                search_with_date.day(self.dateEdit.dateTime().toString("dd-MM-yyyy"))
            )
        else:
            if self.flag == 2:
                text = search_with_date.search_in_week_fast(
                    search_with_date.day(
                        self.dateEdit.dateTime().toString("dd-MM-yyyy")
                    )
                )
            else:
                text = search_with_date.search_in_year(
                    search_with_date.day(
                        self.dateEdit.dateTime().toString("dd-MM-yyyy")
                    )
                )
        self.weather_text.setText(text)
        # self.weather_text.move(515, 230)
        self.weather_text.setFixedWidth(400)


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
