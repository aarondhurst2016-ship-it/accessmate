# Settings management for Talkback Assistant
import json
import os

class Settings:
    def __init__(self):
        self.voice_speed = 1.0
        self.language = 'en'
        self.theme = 'light'
        self.font_size = 12
        self.contrast = 'normal'
        self.weather_city = 'London'
        self.recipe_preference = 'any'
        self.reminder_sound = True
        self.translation_target = 'en'
        self.camera_device = 0
        self.enable_barcode = True
        self.enable_object_detection = True
        self.enable_ocr = True
        self.enable_face_recognition = True
        self.enable_currency_recognition = True
        self.enable_color_recognition = True
        self.enable_pdf_reader = True
        self.enable_word_reader = True
        self.enable_speech_recognition = True
        self.enable_tts = True
        self.enable_app_launch = True
        self.enable_navigation = True
        self.enable_encryption = True
        self.enable_weather = True
        self.enable_reminders = True
        self.enable_accessibility = True
        self.enable_emergency_contact = True
        self.mic_device_index = None
        self.mic_sample_rate = 16000
        self.mic_chunk_size = 1024
        self.mic_timeout = None
        self.skin_tone = "medium"  # Options: fair, medium, dark
        self.body_type = "average"  # Options: slim, average, curvy, athletic
        self.google_maps_api_key = "AIzaSyA8blNy-XibfjrmFMnnrIG_PwMvVf1vEws"  # Google Maps API Key

    def save(self, filename="user_settings.json"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, indent=2)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False

    def load(self, filename="user_settings.json"):
        if not os.path.exists(filename):
            # Create default settings file if missing
            self.save(filename)
            return True
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                setattr(self, k, v)
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False
