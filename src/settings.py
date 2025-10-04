# Settings management for Talkback Assistant
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

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

class SettingsWindow:
    def __init__(self, parent=None):
        self.settings = Settings()
        self.settings.load()
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("AccessMate Settings")
        self.window.geometry("500x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="AccessMate Settings", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Settings sections
        self.create_general_settings(main_frame)
        self.create_accessibility_settings(main_frame)
        self.create_buttons(main_frame)
        
    def create_general_settings(self, parent):
        # General settings frame
        general_frame = ttk.LabelFrame(parent, text="General Settings", padding="10")
        general_frame.pack(fill=tk.X, pady=5)
        
        # Language setting
        lang_frame = ttk.Frame(general_frame)
        lang_frame.pack(fill=tk.X, pady=2)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=self.settings.language)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["en", "es", "fr", "de", "it"])
        lang_combo.pack(side=tk.RIGHT)
        
        # Voice speed setting
        speed_frame = ttk.Frame(general_frame)
        speed_frame.pack(fill=tk.X, pady=2)
        ttk.Label(speed_frame, text="Voice Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=self.settings.voice_speed)
        speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, orient=tk.HORIZONTAL, variable=self.speed_var)
        speed_scale.pack(side=tk.RIGHT)
        
    def create_accessibility_settings(self, parent):
        # Accessibility settings frame
        access_frame = ttk.LabelFrame(parent, text="Accessibility Settings", padding="10")
        access_frame.pack(fill=tk.X, pady=5)
        
        # Font size setting
        font_frame = ttk.Frame(access_frame)
        font_frame.pack(fill=tk.X, pady=2)
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        self.font_var = tk.IntVar(value=self.settings.font_size)
        font_spin = ttk.Spinbox(font_frame, from_=8, to=24, textvariable=self.font_var)
        font_spin.pack(side=tk.RIGHT)
        
        # High contrast setting
        self.contrast_var = tk.BooleanVar(value=self.settings.contrast == 'high')
        ttk.Checkbutton(access_frame, text="High Contrast Mode", variable=self.contrast_var).pack(pady=2, anchor=tk.W)
        
    def create_buttons(self, parent):
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        
    def save_settings(self):
        # Update settings from GUI
        self.settings.language = self.lang_var.get()
        self.settings.voice_speed = self.speed_var.get()
        self.settings.font_size = self.font_var.get()
        self.settings.contrast = 'high' if self.contrast_var.get() else 'normal'
        
        # Save to file
        if self.settings.save():
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Failed to save settings!")
            
    def reset_settings(self):
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.settings = Settings()
            self.settings.save()
            messagebox.showinfo("Settings", "Settings reset to defaults!")
            self.window.destroy()
            
    def show(self):
        self.window.mainloop()
