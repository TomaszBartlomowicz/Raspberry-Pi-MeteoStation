import sys
from plot_window import PlotWindow
from world_weather import WorldWeather
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QWidget,
                             QHBoxLayout,
                             QVBoxLayout, QSizePolicy, QGridLayout, )
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from datetime import datetime
from backend import Backend
from error_console import ErrorConsole


class MainWindow(QMainWindow):
    def __init__(self):
        """Initializes the main application window and its components."""
        super().__init__()
        self.central_widget = QWidget()
        self.dark_mode = True
        self.app = QApplication.instance()

        set_theme(self.app, self.dark_mode)
        self.window_width = 1024
        self.window_height = 600
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.showFullScreen()
        self.resize(1024, 600)

        self.backend = Backend()
        self.error_console = None
        # Buttons
        self.room_temperature = QPushButton(self)
        self.outside_temperature = QPushButton(self)
        self.air_humidity = QPushButton(self)
        self.atmospheric_pressure = QPushButton(self)
        self.rain_detector = QPushButton(self)
        self.online_weather = QPushButton(self)
        self.darkmode_button = QPushButton(self)
        self.darkmode_button.setIcon(QIcon("icons/mode_icon.png"))
        self.warning_button = QPushButton(self)
        self.warning_button.setIcon(QIcon("icons/warning.png"))

        self.all_buttons = [self.room_temperature, self.outside_temperature, self.air_humidity,
                            self.atmospheric_pressure, self.rain_detector, self.online_weather]

        self.weather_buttons = [self.room_temperature, self.outside_temperature, self.air_humidity,
                                self.atmospheric_pressure, self.rain_detector]

        self.buttons_names = ["Temperature", "Outside", "Room Humidity", "Pressure", "Precipitation", "World weather"]
        self.button_icons = ["icons/room.png", "icons/outside.png", "icons/humidity.png",
                             "icons/meter.png", "icons/rain.png", "icons/online.png"]

        # Labels
        self.time_label = QLabel(self)
        self.date_label = QLabel(self)
        self.time_labels = [self.time_label, self.date_label]

        # Setting time and date
        self.current_time = datetime.now()
        self.date = self.current_time.strftime("%d-%m-%y")
        self.time = str(self.current_time.time())[:5]
        self.time_label.setText(self.time)
        self.date_label.setText(self.date)

        # Timer
        self.timer = QTimer()
        self.timer.start(5000)

        self.widget_window = None

        # Initializing functions
        self.declaring_layouts()
        self.updating_weather_parameters()
        self.building_buttons()
        self.button_styling()
        self.sizing_policy()
        self.datetime_style()
        self.connecting_buttons()

    def building_buttons(self):
        """Creates buttons and assigns labels and icons to them."""
        for i in range(6):  # (6 buttons)
            if i == 5:
                self.all_buttons[i].setText("Click here")
            else:
                self.all_buttons[i].setText("loading...")

            button_name_label = QLabel(f'<p style="text-align: center;">{self.buttons_names[i]}</p>', self)
            button_name_label.setStyleSheet("background-color: transparent; font-size: 28px; font-weight: bold;")
            button_name_label.setEnabled(False)

            icon_label = QLabel(self)
            icon_label.setPixmap(QIcon(f"{self.button_icons[i]}").pixmap(60, 60))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background-color: transparent;")

            text_icon_layout = QHBoxLayout()
            text_icon_layout.addStretch(1)
            text_icon_layout.addWidget(icon_label)
            text_icon_layout.addWidget(button_name_label)
            text_icon_layout.addStretch(1)

            button_layout = QVBoxLayout()
            button_layout.addStretch(1)
            button_layout.addLayout(text_icon_layout)
            button_layout.addStretch(4)

            self.all_buttons[i].setLayout(button_layout)

    def updating_weather_parameters(self):
        """Connects functions updating weather data to the timer."""
        self.timer.timeout.connect(lambda: self.backend.update_date_and_time_short(self.time_label, self.date_label))
        self.timer.timeout.connect(lambda: self.backend.get_room_temp(self.all_buttons[0]))
        self.timer.timeout.connect(lambda: self.backend.get_outside_temp(self.all_buttons[1]))
        self.timer.timeout.connect(lambda: self.backend.get_humidity(self.all_buttons[2]))
        self.timer.timeout.connect(lambda: self.backend.get_atm_pressure(self.all_buttons[3]))
        self.timer.timeout.connect(lambda: self.backend.get_rain_info(self.all_buttons[4]))

    def button_styling(self):
        """Styles buttons in the user interface."""
        for button in self.all_buttons:
            button.setStyleSheet("""
                QPushButton {
                        text-align: center;
                        padding: 60px 10px 10px 10px;
                    }
            """)
            button.setFont(QFont("Helvetica"))
        self.darkmode_button.setMinimumSize(20, 20)
        self.darkmode_button.setIconSize(QSize(30, 30))
        self.warning_button.setMinimumSize(20, 20)
        self.warning_button.setIconSize(QSize(30, 30))

    def sizing_policy(self):
        """Sets the size policy for buttons."""
        for button in self.all_buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def datetime_style(self):
        """Applies styling to time and date labels."""
        for label in self.time_labels:
            label.setStyleSheet("font-size: 25px; font-weight: bold;")

    def connecting_buttons(self):
        """Connects buttons to their respective functions."""
        for i in range(len(self.all_buttons)):
            self.all_buttons[i].clicked.connect(lambda _, button_index=i: self.button_clicked(button_index))
        self.darkmode_button.clicked.connect(self.mode_button_clicked)
        self.warning_button.clicked.connect(self.warning_button_clicked)


    def button_clicked(self, button_index):
        """Handles button clicks and opens appropriate windows."""
        button_name = self.buttons_names[button_index]
        theme = set_theme(self.app, self.dark_mode)

        if button_name == "World weather":
            self.widget_window = WorldWeather()
        else:
            self.widget_window = PlotWindow(button_name, self.backend, theme)
        self.widget_window.showFullScreen()
        self.widget_window.resize(1024, 600)

    def mode_button_clicked(self):
        """Toggles between light and dark mode."""
        self.dark_mode = not self.dark_mode
        set_theme(self.app, self.dark_mode)

    def warning_button_clicked(self):
        """Opens Error Console"""
        theme = set_theme(self.app, self.dark_mode)
        self.error_console = ErrorConsole(theme, self.backend)
        self.error_console.showFullScreen()
        self.error_console.resize(1024, 600)

    def declaring_layouts(self):
        """Creates and arranges the GUI layouts."""
        grid_layout = QGridLayout()

        grid_layout.addWidget(self.room_temperature, 0, 0)
        grid_layout.addWidget(self.outside_temperature, 0, 1)
        grid_layout.addWidget(self.air_humidity, 0, 2)
        grid_layout.addWidget(self.atmospheric_pressure, 1, 0)
        grid_layout.addWidget(self.rain_detector, 1, 1)
        grid_layout.addWidget(self.online_weather, 1, 2)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)

        date_time_layout = QHBoxLayout()
        date_time_layout.addWidget(self.date_label)
        date_time_layout.addStretch(1)
        date_time_layout.addWidget(self.time_label)

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.warning_button)
        lower_layout.addStretch(1)
        lower_layout.addWidget(self.darkmode_button)

        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(date_time_layout)
        vertical_layout.addLayout(grid_layout)
        vertical_layout.addLayout(lower_layout)

        self.central_widget.setLayout(vertical_layout)
        self.setCentralWidget(self.central_widget)


def set_theme(app, dark_mode=True):
    """Sets the application's theme based on the dark mode setting."""
    if dark_mode:
        app.setStyleSheet("""
            QWidget { background-color: #2C2F33; color: white; }
            QPushButton { background-color: #293442; color: white; font-size: 35px; font-weight: bold; }
            QLabel { color: #BDC3C7; font-size: 25px; font-weight: bold; }
        """)
        return {"axis_color": "white", "labels_color": "white"}

    else:
        app.setStyleSheet("""
            QWidget { background-color: #b7b6ba; color: black; }
            QPushButton { background-color: #E0E0E0; color: black; font-size: 35px; font-weight: bold; }
            QLabel { color: black; font-size: 25px; font-weight: bold; }
        """)
        return {"axis_color": "black", "labels_color": "black"}

def main():
    app = QApplication(sys.argv)
    set_theme(app, dark_mode=True)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
