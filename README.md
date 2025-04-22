# 🌦️ Raspberry Pi Meteo Station app

A weather monitoring application for Raspberry Pi, written in Python using PyQt5 and PyQtGraph. It tracks local weather conditions using sensors and allows checking the weather in many cities worldwide.

## 🧩 Features

- Measurement of indoor and outdoor temperature
- Reading pressure, humidity, and detecting precipitation
- Real-time weather parameter plotting
- Checking global weather via API
- Light and dark mode interface
- Error console for diagnostics

## 📟 Sensor used:
  
- BME280 (temperature, pressure, humidity)
- DS18B20 (outside temperature)
- YL-83 (rain detection)


## 📷 Screenshots

### Main application window:
![20250326_13h14m28s_grim](https://github.com/user-attachments/assets/e0e6615b-9633-41dc-8d1f-b211bb607d1f)

### Example of data plot:
![20250326_14h45m11s_grim](https://github.com/user-attachments/assets/1ef56bb4-bf7a-4ae8-babb-a9dccb9ed26f)

### Realtime weather in a selected city:

![20250326_13h20m17s_grim](https://github.com/user-attachments/assets/842d94ef-b7ab-412a-9613-e1611ed547d4)

### Error console:

![20250326_13h18m51s_grim](https://github.com/user-attachments/assets/d43ebd6d-3d6d-4700-a02a-0facbc0677f8)



## ⚙️ Installation

### Requirements

- Raspberry Pi with Raspberry Pi OS or Linux OS
- Python 3.9+
- Libraries: PyQt5, PyQtGraph, requests
