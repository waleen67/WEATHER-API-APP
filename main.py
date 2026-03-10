import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt


API_KEY = "PUT_YOUR_API_KEY_HERE"


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter City Name")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")

        self.temperature_label = QLabel("")
        self.emoji_label = QLabel("")
        self.description_label = QLabel("")

        self.initUI()

        self.get_weather_button.clicked.connect(self.get_weather)

    def initUI(self):

        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

    def get_weather(self):

        city = self.city_input.text()

        if not city:
            QMessageBox.warning(self, "Error", "Please enter a city name")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                QMessageBox.warning(self, "Error", data["message"])
                return

            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            weather_id = data["weather"][0]["id"]

            self.temperature_label.setText(f"{temperature} °C")
            self.description_label.setText(description)
            self.emoji_label.setText(self.get_weather_emoji(weather_id))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_weather_emoji(self, weather_id):

        if 200 <= weather_id < 300:
            return "⛈️"
        elif 300 <= weather_id < 400:
            return "🌦️"
        elif 500 <= weather_id < 600:
            return "🌧️"
        elif 600 <= weather_id < 700:
            return "❄️"
        elif 700 <= weather_id < 800:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id < 810:
            return "☁️"


if __name__ == "__main__":

    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
