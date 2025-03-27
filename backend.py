from datetime import datetime
from PyQt5.QtCore import QTimer

""" Imports and declarations for Raspberry PI"""
# from w1thermsensor import W1ThermSensor
# from BME280 import BME280
# import RPi.GPIO as GPIO
# from smbus import SMBus
# from w1thermsensor.errors import SensorNotReadyError, NoSensorFoundError
#
# BUS = SMBus(1)
# BME280 = BME280(i2c_dev=BUS)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(8, GPIO.IN)


class Backend:
    def __init__(self):
        self.data = {
            "room_temp_1h": [],
            "outside_temp_1h": [],
            "humidity_1h": [],
            "pressure_1h": [],
            "rain_1h": [],
            "room_temp_24h": [],
            "outside_temp_24h": [],
            "humidity_24h": [],
            "pressure_24h": [],
            "rain_24h": [],
        }

        self.hours = {
            "time_1h": [],
            "hours_1h": [],
            "time_24h": [],
            "hours_24h": []
        }

        self.timer1 = QTimer()
        self.timer1.start(180000)  # Updates every 3 minutes
        self.timer1.timeout.connect(self.update_data)
        self.errors = []
        self.counter = 0
        self.update_data()

    def add_data(self, key, value, max_length):
        """Adds a new data point to the specified data list, ensuring it does not exceed max_length."""
        if len(self.data[key]) >= max_length:
            self.data[key].pop(0)
        self.data[key].append(value)

    def add_time(self, key, max_length):
        """Adds a timestamp or formatted hour to the corresponding time list, maintaining max_length."""
        real_time = datetime.now()
        reference_time = real_time.timestamp() / 10000000000

        hour = real_time.strftime("%H.%M")
        plot_hour = hour.replace(".", ":")

        if len(self.hours[key]) >= max_length:
            self.hours[key].pop(0)

        if key in ["time_1h", "time_24h"]:
            self.hours[key].append(reference_time)
        elif key in ["hours_1h", "hours_24h"]:
            self.hours[key].append(plot_hour)

    def update_data(self):
        """Loads weather data, updates hourly and daily logs, and stores time references."""
        try:
            room_temperature = BME280.get_temperature()
            outside_temperature = W1ThermSensor().get_temperature()
            pressure = BME280.get_pressure()
            humidity = BME280.get_humidity()
            if GPIO.input(8) == GPIO.LOW:
                rain = 1
            else:
                rain = 0

            self.add_data("room_temp_1h", room_temperature, 20)
            self.add_data("outside_temp_1h", outside_temperature, 20)
            self.add_data("humidity_1h", humidity, 20)
            self.add_data("pressure_1h", pressure, 20)
            self.add_data("rain_1h", rain, 20)
            self.add_time("hours_1h", 20)
            self.add_time("time_1h", 20)
            self.counter += 1
            print(self.counter)

            if self.counter == 1 or self.counter % 10 == 0:
                self.add_data("room_temp_24h", room_temperature, 20)
                self.add_data("outside_temp_24h", outside_temperature, 20)
                self.add_data("humidity_24h", humidity, 20)
                self.add_data("pressure_24h", pressure, 20)
                self.add_data("rain_24h", rain, 20)
                self.add_time("hours_24h", 20)
                self.add_time("time_24h", 20)
        except Exception as e:
            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M")
            error_message = (f"At {formatted_now} {type(e).__name__} occurred when plotting weather parametres. \n"
                             f"No values were plotted on a graph at the mentioned time")
            self.errors.append(error_message)

    def get_room_temp(self, button):
        """Gets and updates room temperature reading"""
        try:
            reading = BME280.get_temperature()
            temperature = str(round(reading, 2))
            button.setText(temperature + chr(176) + "C")
        except OSError:
            button.setText("no sensor found")
        except NameError:
            button.setText("library error")

    def get_outside_temp(self, button):
        """Gets and updates outside temperature reading"""
        try:
            sensor = W1ThermSensor()
            reading = sensor.get_temperature()
            temperature = str(round(reading, 2))
            button.setText(temperature + chr(176) + "C")
        except NameError:
            button.setText("library error")
        except SensorNotReadyError:
            button.setText("sensor not ready")
        except NoSensorFoundError:
            button.setText("no sensor found")
        except Exception as e:
            button.setText(type(e).__name__)

    def get_humidity(self, button):
        """Gets and updates humidity reading"""
        try:
            reading = BME280.get_humidity()
            humidity = str(round(reading, 2))
            button.setText(f"{humidity}%")
        except OSError:
            button.setText("no sensor found")
        except NameError:
            button.setText("library error")
        except Exception as e:
            button.setText(type(e).__name__)

    def get_atm_pressure(self, button):
        """Gets and updates pressure reading"""
        try:
            reading = BME280.get_pressure()
            pressure = str(round(reading, 2))
            button.setText(f"{pressure} hPa")
        except OSError:
            button.setText("no sensor found")
        except NameError:
            button.setText("library error")
        except Exception as e:
            button.setText(type(e).__name__)

    def get_rain_info(self, button):
        """
        Checks state on GPIO pin to determine weather or nor rain has been detected
        Updates rain info in main window
        """
        try:
            if GPIO.input(8) == GPIO.LOW:
                button.setText('Rain detected')
            else:
                button.setText('No rain')
        except NameError:
            button.setText("library error")
        except Exception as e:
            button.setText(type(e).__name__)

    def update_date_and_time(self, time_label, date_label):
        """Updates the displayed date and time labels."""
        real_time = datetime.now()
        hour = str(real_time.time())[:8]
        date = real_time.strftime("%d-%m-%Y")
        time_label.setText(hour)
        date_label.setText(date)

    def update_date_and_time_short(self, time_label, date_label):
        """Updates the displayed date and time labels with a shorter time format (HH:MM)."""
        real_time = datetime.now()
        hour = str(real_time.time())[:5]
        date = real_time.strftime("%d-%m-%y")
        time_label.setText(hour)
        date_label.setText(date)
