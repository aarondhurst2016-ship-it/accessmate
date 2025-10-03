import json
import os

class Settings:
    def __init__(self):
        self.voice_speed = 1.0
        self.language = 'en'
        self.theme = 'light'
        self.font_size = 12
        self.weather_city = 'London'

    def save(self, filename="settings.json"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False

    def load(self, filename="settings.json"):
        if not os.path.exists(filename):
            return False
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                setattr(self, k, v)
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False
