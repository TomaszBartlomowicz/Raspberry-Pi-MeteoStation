import requests
from PyQt5.QtWidgets import (QLabel, QPushButton, QWidget, QHBoxLayout,
                             QVBoxLayout, QSizePolicy, QGridLayout, QComboBox )
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from dotenv import load_dotenv
import os

class WorldWeather(QWidget):
    def __init__(self):
        super().__init__()

        self.window_width = 1024
        self.window_height = 600
        self.setGeometry(0, 0, self.window_width, self.window_height)


        # Some Well-Known Capitals Around the World
        self.world_capitals = [
            "Abu Dhabi", "Amman", "Amsterdam", "Ankara", "Athens", "Baghdad", "Bangkok", "Beijing", "Belgrade",
            "Berlin", "Bogota", "Brasilia", "Brussels", "Bucharest", "Budapest", "Buenos Aires", "Cairo",
            "Canberra", "Caracas", "Copenhagen", "Doha", "Dublin", "Hanoi", "Helsinki", "Istanbul",
            "Jakarta", "Kabul", "Kuala Lumpur", "Lisbon", "London", "Madrid", "Manila", "Mexico City",
            "Moscow", "New Delhi", "Oslo", "Ottawa", "Paris", "Prague", "Reykjavik", "Riyadh", "Rome",
            "Santiago", "Seoul", "Singapore", "Sofia", "Stockholm", "Tehran", "Tokyo", "Vienna", "Warsaw",
            "Washington", "Zagreb"
        ]


        self.poland_cities = [
            "Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań", "Gdańsk", "Szczecin",
            "Bydgoszcz", "Lublin", "Katowice", "Białystok", "Gdynia", "Częstochowa",
            "Radom", "Sosnowiec", "Toruń", "Kielce", "Gliwice", "Zabrze", "Olsztyn",
            "Rzeszów", "Zielona Góra", "Bytom", "Nowy Sącz", "Wałbrzych", "Opole",
            "Płock", "Elbląg", "Gorzów Wielkopolski", "Dąbrowa Górnicza", "Tarnów",
            "Kalisz", "Legnica", "Świdnica", "Mielec", "Przemyśl", "Stalowa Wola",
            "Lubin", "Tychy", "Chorzów", "Ruda Śląska", "Siedlce", "Włocławek",
            "Ciechanów", "Kołobrzeg", "Lubliniec", "Zamość", "Żory", "Piotrków Trybunalski",
            "Kędzierzyn-Koźle", "Suwalki", "Świnoujście", "Krosno", "Kutno", "Kielce", "Głogów"
        ]

        self.city_label = QLabel("Select city name: ", self)
        self.city_list = QComboBox(self)
        self.city_list.addItems(self.poland_cities)

        self.weather_description = QLabel(self)
        self.weather_icon_label = QLabel(self)

        self.temperature_label = QLabel(self)
        self.wind_label = QLabel(self)
        self.pressure_label = QLabel(self)
        self.humidity_label = QLabel(self)
        self.weather_parameters_labels = [self.temperature_label, self.wind_label, self.pressure_label, self.humidity_label]


        self.temp_icon_label = QLabel(self)
        self.wind_icon_label = QLabel(self)
        self.press_icon_label = QLabel(self)
        self.hum_icon_label = QLabel(self)

        self.temp_icon_label.setPixmap(QIcon("icons/outside.png").pixmap(70, 70))
        self.wind_icon_label.setPixmap(QIcon("icons/wind_icon.png").pixmap(70, 70))
        self.press_icon_label.setPixmap(QIcon("icons/meter.png").pixmap(70, 70))
        self.hum_icon_label.setPixmap(QIcon("icons/humidity.png").pixmap(70, 70))

        self.icon_labels = [self.temp_icon_label, self.wind_icon_label, self.press_icon_label, self.hum_icon_label, self.weather_icon_label]

        # Text Labels
        self.temperature = QLabel("Temperature", self)
        self.wind_speed = QLabel("Wind speed", self)
        self.pressure = QLabel("Pressure", self)
        self.humidity = QLabel("Humidity", self)
        self.text_labels = [self.temperature, self.wind_speed, self.pressure, self.humidity]


        self.poland_selected = True
        # Buttons
        self.back_button = QPushButton("Main menu", self)
        self.get_weather_button = QPushButton("Check Weather!", self)
        self.choose_region_button = QPushButton(self)
        self.choose_region_button.setIcon(QIcon("icons/poland.png"))
        self.choose_region_button.setIconSize(QSize(90, 40))


        self.back_button.clicked.connect(self.close)
        self.get_weather_button.clicked.connect(self.get_weather)
        self.choose_region_button.clicked.connect(self.choosing_region)

        self.init_ui()
        self.styling()

    def init_ui(self):
        """Manages layouts"""
        main_layout = QVBoxLayout()

        labels_layout = QGridLayout()

        labels_layout.addWidget(self.temperature_label, 2, 0)
        labels_layout.addWidget(self.wind_label, 2, 1)
        labels_layout.addWidget(self.pressure_label, 2, 2)
        labels_layout.addWidget(self.humidity_label, 2, 3)
        labels_layout.addWidget(self.temp_icon_label, 1, 0)
        labels_layout.addWidget(self.wind_icon_label, 1, 1)
        labels_layout.addWidget(self.press_icon_label, 1, 2)
        labels_layout.addWidget(self.hum_icon_label, 1, 3)
        labels_layout.addWidget(self.temperature, 0, 0)
        labels_layout.addWidget(self.wind_speed, 0, 1)
        labels_layout.addWidget(self.pressure, 0, 2)
        labels_layout.addWidget(self.humidity, 0, 3)

        labels_layout.setRowStretch(0, 2)
        labels_layout.setRowStretch(1, 1)
        labels_layout.setRowStretch(2, 1)
        labels_layout.setColumnStretch(0, 3)
        labels_layout.setColumnStretch(1, 3)
        labels_layout.setColumnStretch(2, 3)
        labels_layout.setColumnStretch(3, 3)


        selecting_layout = QHBoxLayout()
        selecting_layout.addWidget(self.choose_region_button, stretch=1)
        selecting_layout.addWidget(self.city_list, 10)
        selecting_layout.addStretch(1)

        check_layout = QHBoxLayout()
        check_layout.addStretch(1)
        check_layout.addWidget(self.get_weather_button, 10)
        check_layout.addStretch(1)

        main_layout.addWidget(self.city_label)
        main_layout.addStretch(1)
        main_layout.addLayout(selecting_layout)
        main_layout.addLayout(check_layout, 2)
        main_layout.addStretch(1)
        main_layout.addWidget(self.weather_description)
        main_layout.addWidget(self.weather_icon_label)
        main_layout.addStretch(1)
        main_layout.addLayout(labels_layout)
        main_layout.addStretch(2)
        main_layout.addWidget(self.back_button)
        self.setLayout(main_layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignCenter)

    def choosing_region(self):
        self.poland_selected = not self.poland_selected
        if self.poland_selected:
            self.choose_region_button.setIcon(QIcon("icons/poland.png"))
            self.city_list.clear()
            self.city_list.addItems(self.poland_cities)
        else:
            self.choose_region_button.setIcon(QIcon("icons/earth.png"))
            self.city_list.clear()
            self.city_list.addItems(self.world_capitals)

    def styling(self):
        self.city_list.view().setVerticalScrollBarPolicy(0)
        for each_label in self.weather_parameters_labels:
            each_label.setStyleSheet("color: #b3221d;"
                                     "font-size: 30px;"
                                     "font-weight: bold;"
                                     )
            each_label.setAlignment(Qt.AlignCenter)

        for each_label in self.icon_labels:
            each_label.setAlignment(Qt.AlignCenter)

        for each_label in self.text_labels:
            each_label.setStyleSheet(
                                    "font-size: 32px;"
                                    "font-weight: bold;"
                                     )
            each_label.setAlignment(Qt.AlignCenter)

        self.get_weather_button.setStyleSheet("font-size: 40px;"
                                              "font-weight: bold;")

        self.city_list.setStyleSheet("font-size: 40px;"
                                     "font-weight: bold;")


        self.weather_description.setStyleSheet("font-size: 40px;"
                                                "font-weight: bold;"
                                                "color: #3aa11b;")

        self.city_label.setStyleSheet("font-size: 50px;"
                                      "font-weight: bold;")

        self.back_button.setStyleSheet("font-size: 20px;"
                                       "font-weight: bold;")

        self.get_weather_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def get_weather(self):
        """Downloads info through api key and manages possible errors"""
        load_dotenv("keys.env")
        api_key = os.getenv("API_KEY")
        city_name = self.city_list.currentText()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.check_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 401:
                    self.error_message("Unauthorized")
                case 403:
                    self.error_message("Acces is denied")
                case 500:
                    self.error_message("Internal server Error")
                case 502:
                    self.error_message("Bad Gateway")
                case 503:
                    self.error_message("Server is down")
                case _:
                    self.error_message("HTTP error")

        except requests.exceptions.ConnectionError:
            self.error_message("No internter connection ")
        except requests.exceptions.Timeout:
            self.error_message("Timeout Error")
        except requests.exceptions.TooManyRedirects:
            self.error_message("Too many redirects")
        except requests.exceptions.RequestException:
            self.error_message("Request Error")


    def check_weather(self, data):
        """Displays weather for the chosen city"""
        icon = str(data["weather"][0]["icon"])
        emoji_link = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        downloaded_emoji = requests.get(emoji_link)
        pixmap = QPixmap()
        pixmap.loadFromData(downloaded_emoji.content)

        temp_in_celcius = round(data["main"]["temp"] - 273.15, 2)
        weather_description = str(data["weather"][0]["description"])
        capitalized = weather_description.capitalize()

        self.temperature_label.setText(str(temp_in_celcius) + chr(176) + "C")
        self.wind_label.setText(str(data["wind"]["speed"])+ " m/s")
        self.humidity_label.setText(str(data["main"]["humidity"]) + "%")
        self.pressure_label.setText(str(data["main"]["pressure"]) + " hpa")

        self.weather_description.setText(capitalized)
        self.weather_icon_label.setPixmap(pixmap)

    def error_message(self, message):
        self.weather_description.setText(message)

