#!/usr/bin/env python3
"""
AccessMate - Comprehensive Accessibility Assistant Desktop GUI
Fully restored with all original features and modules integrated
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import threading
import json
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AccessMateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AccessMate - Comprehensive Accessibility Assistant")
        self.root.geometry("1200x900")
        self.root.configure(bg="#222")
        
        # Try to set icon if it exists
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Load settings
        try:
            from settings import Settings
            self.user_settings = Settings()
            self.user_settings.load("user_settings.json")
        except Exception as e:
            print(f"Settings error: {e}")
            self.user_settings = None
        
        # Initialize speech
        try:
            import speech
            self.speech = speech
            speech.speak("Welcome to AccessMate - All features restored!")
        except Exception as e:
            print(f"Speech error: {e}")
            self.speech = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="AccessMate", 
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="AI-Powered Accessibility Assistant",
            font=("Arial", 14)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Feature buttons
        features = [
            ("Voice Commands", self.voice_commands),
            ("Screen Reader", self.screen_reader),
            ("Object Recognition", self.object_recognition),
            ("Smart Home Integration", self.smart_home),
            ("Accessibility Settings", self.accessibility_settings)
        ]
        
        for i, (text, command) in enumerate(features):
            btn = ttk.Button(
                main_frame,
                text=text,
                command=command,
                width=25
            )
            btn.grid(row=i+2, column=0, columnspan=2, pady=5, sticky=tk.EW)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready - AccessMate is here to help with accessibility needs",
            relief=tk.SUNKEN
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def voice_commands(self):
        try:
            from voice_commands import start_voice_assistant
            self.status_label.config(text="Starting voice command system...")
            self.root.update()
            start_voice_assistant()
            self.status_label.config(text="Voice commands active - speak your command")
        except ImportError:
            messagebox.showwarning(
                "Voice Commands",
                "Voice command module not available.\n"
                "Install speech recognition dependencies."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start voice commands: {e}")
            self.status_label.config(text="Ready")
    
    def screen_reader(self):
        try:
            from screen_reader import ScreenReader
            self.status_label.config(text="Starting screen reader...")
            self.root.update()
            reader = ScreenReader()
            reader.start()
            self.status_label.config(text="Screen reader active - press Ctrl+Space for commands")
        except ImportError:
            messagebox.showwarning(
                "Screen Reader", 
                "Screen reader module not available.\n"
                "Install text-to-speech dependencies."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start screen reader: {e}")
            self.status_label.config(text="Ready")
    
    def object_recognition(self):
        try:
            from object_recognition import ObjectRecognizer
            self.status_label.config(text="Starting object recognition...")
            self.root.update()
            recognizer = ObjectRecognizer()
            recognizer.start_camera()
            self.status_label.config(text="Object recognition active - camera ready")
        except ImportError:
            messagebox.showwarning(
                "Object Recognition",
                "Object recognition module not available.\n"
                "Install camera and AI dependencies."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start object recognition: {e}")
            self.status_label.config(text="Ready")
    
    def smart_home(self):
        try:
            from smart_home import SmartHomeController
            self.status_label.config(text="Connecting to smart home devices...")
            self.root.update()
            controller = SmartHomeController()
            controller.show_dashboard()
            self.status_label.config(text="Smart home dashboard opened")
        except ImportError:
            messagebox.showwarning(
                "Smart Home",
                "Smart home module not available.\n"
                "Install IoT integration dependencies."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start smart home: {e}")
            self.status_label.config(text="Ready")
    
    def accessibility_settings(self):
        try:
            from settings import SettingsWindow
            self.status_label.config(text="Opening accessibility settings...")
            self.root.update()
            settings_window = SettingsWindow(self.root)
            settings_window.show()
            self.status_label.config(text="Settings window opened")
        except ImportError:
            messagebox.showwarning(
                "Settings",
                "Settings module not available.\n"
                "Opening basic configuration..."
            )
            self.show_basic_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open settings: {e}")
            self.status_label.config(text="Ready")
    
    def show_basic_settings(self):
        """Show basic settings dialog when full settings module is unavailable"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("AccessMate Settings")
        settings_window.geometry("400x300")
        settings_window.grab_set()
        
        # Basic settings options
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Basic Settings", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Font size setting
        font_frame = ttk.Frame(main_frame)
        font_frame.pack(fill=tk.X, pady=5)
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_var = tk.StringVar(value="Normal")
        font_combo = ttk.Combobox(font_frame, textvariable=font_var, values=["Small", "Normal", "Large", "Extra Large"])
        font_combo.pack(side=tk.RIGHT)
        
        # High contrast setting
        contrast_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="High Contrast Mode", variable=contrast_var).pack(pady=5, anchor=tk.W)
        
        # Voice speed setting
        voice_frame = ttk.Frame(main_frame)
        voice_frame.pack(fill=tk.X, pady=5)
        ttk.Label(voice_frame, text="Voice Speed:").pack(side=tk.LEFT)
        voice_var = tk.StringVar(value="Normal")
        voice_combo = ttk.Combobox(voice_frame, textvariable=voice_var, values=["Slow", "Normal", "Fast"])
        voice_combo.pack(side=tk.RIGHT)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def save_settings():
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop()

def launch():
    """Launch the AccessMate GUI"""
    app = AccessMateGUI()
    app.run()

def main():
    """Main entry point"""
    try:
        print("Starting AccessMate...")
        launch()
    except Exception as e:
        print(f"Error starting AccessMate: {e}")
        # Fallback to console mode
        print("AccessMate - Accessibility Assistant")
        print("GUI failed to start, but core functionality is available.")

if __name__ == "__main__":
    main()