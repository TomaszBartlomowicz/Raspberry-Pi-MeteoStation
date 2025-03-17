from PyQt5.QtWidgets import (QLabel, QPushButton, QWidget, QHBoxLayout,
                             QVBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from datetime import datetime
import pyqtgraph as pg


class PlotWindow(QWidget):
    def __init__(self, button_name, backend, theme):
        """Initializes the plot window with UI elements and settings."""
        super().__init__()

        self.central_widget = QWidget()
        self.window_width = 1024
        self.window_height = 600
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.button_name = button_name
        self.theme = theme
        self.backend = backend
        self.axis_name = None
        self.plot_choice = "1h"

        if self.button_name == "Temperature" or self.button_name == "Outside":
            self.axis_name = "Temperature (°C)"
        elif self.button_name == "Room Humidity":
            self.axis_name = "Humidity (%)"
        elif self.button_name == "Pressure":
            self.axis_name = "Pressure (hPa)"
        elif self.button_name == "Precipitation":
            self.axis_name = "Rain"

        # Time and date labels
        self.time_label = QLabel(self)
        self.date_label = QLabel(self)
        self.time_date_labels = [self.time_label, self.date_label]

        self.current_time = datetime.now()
        self.date = self.current_time.strftime("%d-%m-%Y")
        self.time = str(self.current_time.time())[:8]
        self.time_label.setText(self.time)
        self.date_label.setText(self.date)

        # Main text label (Button Name)
        self.description_label = QLabel(self)
        self.description_label.setText(f"{button_name}")
        self.description_label.setStyleSheet("font-size: 45px; font-weight: bold;")
        self.description_label.setFont(QFont("Helvetica"))

        # Buttons
        self.return_button = QPushButton("Back", self)
        self.one_hour_button = QPushButton("1H", self)
        self.hour_24_button = QPushButton("12H", self)
        self.buttons = [self.return_button, self.one_hour_button, self.hour_24_button]
        self.return_button.clicked.connect(self.close)

        # Setting Timers
        self.timer = QTimer()
        self.timer2 = QTimer()
        self.timer.start(1000)
        self.timer2.start(60000)

        # Declaring plot
        self.parameters_plot = pg.PlotWidget()

        # Functions
        self.updating_plot()
        self.creating_layouts()
        self.button_style()
        self.connecting_to_timers()
        self.connecting_buttons()
        self.time_labels_style()
        self.button_style()
        self.creating_plot()

    def button_style(self):
        """Applies styling to buttons."""
        for each_button in self.buttons:
            each_button.setStyleSheet("""
                QPushButton {
                        font-size: 18px;
                        font-weight: bold;
                        text-align: center;
                 } 
            """)

    def time_labels_style(self):
        """Applies styling to time and date labels."""
        for each_label in self.time_date_labels:
            each_label.setStyleSheet("font-size: 25px; font-weight: bold;")

    def connecting_to_timers(self):
        """Connects timers to update time and plot periodically."""
        self.timer.timeout.connect(lambda: self.backend.update_date_and_time(self.time_label, self.date_label))
        self.timer2.timeout.connect(self.updating_plot)

    def connecting_buttons(self):
        """Connects buttons to appropriate functions."""
        self.one_hour_button.clicked.connect(self.one_hour_clicked)
        self.hour_24_button.clicked.connect(self.hour_24_clicked)

    def one_hour_clicked(self):
        """Handles click event for 1H button."""
        self.plot_choice = "1h"
        print(f"Plot choice changed to: {self.plot_choice}")
        self.updating_plot()

    def hour_24_clicked(self):
        """Handles click event for 24H button."""
        self.plot_choice = "24h"
        print(f"Plot choice changed to: {self.plot_choice}")
        self.updating_plot()

    def configure_axis(self, axis, font_size=12):
        """Configures axis appearance with font size and colors."""
        axis.setTickFont(pg.QtGui.QFont('Arial', font_size))
        axis.setTextPen(pg.mkPen(self.theme["labels_color"]))
        axis.setPen(pg.mkPen(color=self.theme["axis_color"], width=2))

    def creating_plot(self):
        """Creates and configures the plot widget."""
        labels_color = self.theme["labels_color"]
        styles = {"font-size": "25px", "font-weight": "bold", "color": labels_color}
        self.parameters_plot.setBackground("transparent")
        x_axis = self.parameters_plot.getAxis('bottom')
        y_axis = self.parameters_plot.getAxis('left')
        self.configure_axis(x_axis, font_size=10)
        self.configure_axis(y_axis, font_size=10)
        self.parameters_plot.setLabel("bottom", "Time", **styles)
        self.parameters_plot.setLabel("left", self.axis_name, **styles)

    def updating_plot(self):
        """Updates the plot with new data based on the selected time range."""

        time_key = "time_1h" if self.plot_choice == "1h" else "time_24h"
        plot_colors = {"Temperature": "#b3221d",
                       "Outside": "#e06016",
                       "Room Humidity": "#1c2d9c",
                       "Pressure": "#3aa11b",
                       "Precipitation": "#7f18a1"}
        plotted_data = {"Temperature": "room_temp",
                        "Outside": "outside_temp",
                        "Room Humidity": "humidity",
                        "Pressure": "pressure",
                        "Precipitation": "rain"}
        plotted_data_key = plotted_data.get(self.button_name)
        plot_color_key = plot_colors.get(self.button_name)
        hour_labels = [(time, label) for time, label in
                       zip(self.backend.hours["time_1h"], self.backend.hours["hours_1h"])]
        x_axis = self.parameters_plot.getAxis('bottom')
        x_axis.setTicks([hour_labels])
        self.parameters_plot.plot(
            self.backend.hours[time_key],
            self.backend.data[f"{plotted_data_key}_{self.plot_choice}"],
            pen=pg.mkPen(color=plot_color_key, width=4),
            symbol='o', symbolSize=9,
            symbolBrush=plot_color_key,
            clear=True)

    def creating_layouts(self):
        date_time_layout = QHBoxLayout()
        date_time_layout.addWidget(self.date_label)
        date_time_layout.addStretch(25)
        date_time_layout.addWidget(self.time_label)

        description_layout = QHBoxLayout()
        description_layout.addStretch(1)
        description_layout.addWidget(self.description_label)
        description_layout.addStretch(1)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.one_hour_button)
        buttons_layout.addWidget(self.hour_24_button)

        plot_layout = QHBoxLayout()
        #plot_layout.addStretch(1)
        plot_layout.addWidget(self.parameters_plot, stretch=20)
        plot_layout.addStretch(1)

        return_button_layout = QHBoxLayout()
        # return_button_layout.addStretch(2)
        return_button_layout.addLayout(buttons_layout)
        return_button_layout.addStretch(2)
        return_button_layout.addWidget(self.return_button)

        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(date_time_layout)

        vertical_layout.addLayout(description_layout)

        vertical_layout.addStretch(1)
        vertical_layout.addLayout(plot_layout)
        vertical_layout.addStretch(1)
        vertical_layout.addLayout(return_button_layout)
        self.setLayout(vertical_layout)
