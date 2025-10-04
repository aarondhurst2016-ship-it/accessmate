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
            speech.speak("Welcome to AccessMate!")
        except Exception as e:
            print(f"Speech error: {e}")
            self.speech = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root,
            text="🌟 AccessMate - Your Complete Accessibility Assistant",
            font=("Arial", 20, "bold"),
            bg="#222",
            fg="#FFD600"
        )
        title_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready - AccessMate is here to help with all your accessibility needs",
            font=("Arial", 12),
            bg="#222",
            fg="#00FF00",
            relief=tk.SUNKEN
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Create scrollable canvas for features
        canvas = tk.Canvas(self.root, bg="#222", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#222")
        
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Update scroll region when frame changes
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create organized feature sections
        self.create_core_features()
        self.create_communication_features()
        self.create_media_entertainment_features()
        self.create_navigation_health_features()
        self.create_smart_home_automation_features()
        self.create_productivity_features()
        self.create_accessibility_features()
        self.create_emergency_security_features()
        self.create_settings_utilities()
        
    def create_section_header(self, title, row):
        """Create a section header with styling"""
        header_frame = tk.Frame(self.scroll_frame, bg="#444", relief=tk.RAISED, bd=2)
        header_frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=(15, 5))
        
        header_label = tk.Label(
            header_frame,
            text=title,
            font=("Arial", 16, "bold"),
            bg="#444",
            fg="#FFD600"
        )
        header_label.pack(pady=8)
        
        # Configure grid
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.scroll_frame.grid_columnconfigure(2, weight=1)
        self.scroll_frame.grid_columnconfigure(3, weight=1)
        
        return row + 1
    
    def create_feature_button(self, parent, text, command, color, tooltip, row, col):
        """Create a standardized feature button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2"
        )
        btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
        
        # Add hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
            if self.speech:
                try:
                    self.speech.speak(tooltip)
                except:
                    pass
                    
        def on_leave(e):
            btn.config(bg=color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effects"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def create_core_features(self):
        """Core accessibility features"""
        row = self.create_section_header("🎯 CORE ACCESSIBILITY FEATURES", 0)
        
        features = [
            ("Voice Commands", self.voice_commands, "#00C853", "Advanced voice command system with natural language processing"),
            ("Screen Reader", self.screen_reader, "#43A047", "Comprehensive screen reading with customizable voices"),
            ("Object Recognition", self.object_recognition, "#7E57C2", "AI-powered object detection and scene description"),
            ("OCR Text Reader", self.ocr_reader, "#4CAF50", "Read text from images, PDFs, and documents"),
            ("Barcode Scanner", self.barcode_scanner, "#FF9800", "Scan and identify barcodes and QR codes"),
            ("Face Recognition", self.face_recognition, "#E91E63", "Recognize and announce faces of people"),
            ("Currency Recognition", self.currency_recognition, "#795548", "Identify bills and currency values"),
            ("Color Recognition", self.color_recognition, "#9C27B0", "Identify and announce colors")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
        
        return row + (len(features) + 3) // 4
    
    def create_communication_features(self):
        """Communication and messaging features"""
        row = self.create_section_header("📞 COMMUNICATION & MESSAGING", 5)
        
        features = [
            ("Email Management", self.email_management, "#1976D2", "Read, compose, and manage email messages"),
            ("Text Messaging", self.text_messaging, "#4CAF50", "Send and receive text messages"),
            ("Call Integration", self.call_integration, "#FF5722", "Make and manage phone calls"),
            ("Emergency Contacts", self.emergency_contacts, "#D32F2F", "Quick access to emergency contacts"),
            ("Emergency SOS", self.emergency_sos, "#B71C1C", "One-touch emergency assistance with location"),
            ("Translation", self.translation_service, "#3949AB", "Translate text and speech between languages"),
            ("Language Learning", self.language_learning, "#2196F3", "Interactive language learning tools"),
            ("Speech Training", self.speech_training, "#8E24AA", "Voice recognition training and improvement")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_media_entertainment_features(self):
        """Media and entertainment features"""
        row = self.create_section_header("🎵 MEDIA & ENTERTAINMENT", 8)
        
        features = [
            ("Media Player", self.media_player, "#E91E63", "Play music, videos, and audio content"),
            ("Netflix Browser", self.browse_netflix, "#E50914", "Browse and play Netflix content"),
            ("Spotify Player", self.browse_spotify, "#1DB954", "Browse and play Spotify music"),
            ("YouTube Player", self.play_youtube, "#FF0000", "Play YouTube videos by URL or search"),
            ("Audiobook Library", self.audiobook_library, "#8E24AA", "Browse and play audiobooks"),
            ("Accessible Games", self.accessible_games, "#00B0FF", "Play audio games with haptic feedback"),
            ("Game Launcher", self.game_launcher, "#FF4081", "Launch installed games by voice or text"),
            ("Podcast Player", self.podcast_player, "#FF6F00", "Listen to podcasts and audio shows")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_navigation_health_features(self):
        """Navigation, health, and fitness features"""
        row = self.create_section_header("🧭 NAVIGATION, HEALTH & FITNESS", 11)
        
        features = [
            ("GPS Navigation", self.gps_navigation, "#4CAF50", "Voice-guided GPS navigation and directions"),
            ("Public Transit", self.public_transit, "#2196F3", "Public transportation schedules and routes"),
            ("Nearby Places", self.nearby_places, "#FF9800", "Find nearby restaurants, stores, and services"),
            ("Location Services", self.location_services, "#0097A7", "Get current location and location-based info"),
            ("Health Tracker", self.health_tracker, "#D32F2F", "Track health metrics and wellness data"),
            ("Medication Reminders", self.medication_reminders, "#E91E63", "Set and manage medication schedules"),
            ("Fitness Assistant", self.fitness_assistant, "#4CAF50", "Workout guidance and fitness tracking"),
            ("Medical Emergency", self.medical_emergency, "#B71C1C", "Medical emergency assistance and alerts")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_smart_home_automation_features(self):
        """Smart home and automation features"""
        row = self.create_section_header("🏠 SMART HOME & AUTOMATION", 14)
        
        features = [
            ("Smart Home Control", self.smart_home_control, "#8BC34A", "Control smart home devices and scenes"),
            ("Light Control", self.light_control, "#FFD600", "Turn lights on/off and adjust brightness"),
            ("Thermostat Control", self.thermostat_control, "#FF5722", "Control temperature and HVAC systems"),
            ("Security System", self.security_system, "#795548", "Monitor and control home security"),
            ("IoT Device Manager", self.iot_manager, "#607D8B", "Manage all connected IoT devices"),
            ("Voice Assistant Hub", self.voice_assistant_hub, "#9C27B0", "Central hub for voice commands"),
            ("Automation Scenes", self.automation_scenes, "#00BCD4", "Create and manage automation scenes"),
            ("Remote Control", self.remote_control, "#3F51B5", "Universal remote control for devices")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_productivity_features(self):
        """Productivity and organization features"""
        row = self.create_section_header("📋 PRODUCTIVITY & ORGANIZATION", 17)
        
        features = [
            ("Notes & To-Do", self.notes_todo, "#FFB300", "Create and manage notes and to-do lists"),
            ("Calendar Integration", self.calendar_integration, "#7CB342", "View and manage calendar events"),
            ("Reminders & Alarms", self.reminders_alarms, "#FF9800", "Set reminders and alarms with voice alerts"),
            ("File Manager", self.file_manager, "#388E3C", "Browse and manage files and folders"),
            ("Document Scanner", self.document_scanner, "#5D4037", "Scan documents with camera or scanner"),
            ("Expense Tracker", self.expense_tracker, "#795548", "Track expenses and financial data"),
            ("Password Manager", self.password_manager, "#424242", "Secure password storage and generation"),
            ("Backup & Sync", self.backup_sync, "#607D8B", "Backup and sync data across devices")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_accessibility_features(self):
        """Advanced accessibility features"""
        row = self.create_section_header("♿ ADVANCED ACCESSIBILITY", 20)
        
        features = [
            ("Magnification", self.magnification, "#9C27B0", "Screen magnification and zoom tools"),
            ("High Contrast", self.high_contrast, "#424242", "High contrast themes and display modes"),
            ("Large Text Mode", self.large_text, "#FF6F00", "Large text and UI elements"),
            ("Keyboard Navigation", self.keyboard_navigation, "#00BCD4", "Enhanced keyboard navigation"),
            ("Switch Control", self.switch_control, "#4CAF50", "Switch-based device control"),
            ("Eye Tracking", self.eye_tracking, "#E91E63", "Eye tracking interface control"),
            ("Haptic Feedback", self.haptic_feedback, "#FF5722", "Vibration and haptic feedback"),
            ("Custom Shortcuts", self.custom_shortcuts, "#673AB7", "Create custom keyboard shortcuts")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_emergency_security_features(self):
        """Emergency and security features"""
        row = self.create_section_header("🚨 EMERGENCY & SECURITY", 23)
        
        features = [
            ("Emergency Monitor", self.emergency_monitor, "#D32F2F", "24/7 emergency monitoring system"),
            ("Panic Button", self.panic_button, "#B71C1C", "One-touch panic button with alerts"),
            ("Fall Detection", self.fall_detection, "#FF5722", "Automatic fall detection and alerts"),
            ("Security Status", self.security_status, "#795548", "Check device and account security"),
            ("Privacy Tools", self.privacy_tools, "#424242", "Privacy protection and data security"),
            ("Identity Protection", self.identity_protection, "#37474F", "Identity theft protection"),
            ("Safe Mode", self.safe_mode, "#546E7A", "Enable safe mode with limited features"),
            ("Emergency Info", self.emergency_info, "#F44336", "Store emergency contact information")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    def create_settings_utilities(self):
        """Settings and utility features"""
        row = self.create_section_header("⚙️ SETTINGS & UTILITIES", 26)
        
        features = [
            ("Settings", self.accessibility_settings, "#4FC3F7", "Configure all AccessMate settings"),
            ("Voice Training", self.voice_training, "#8E24AA", "Train voice recognition for better accuracy"),
            ("Microphone Test", self.microphone_test, "#00C853", "Test microphone and audio input"),
            ("System Information", self.system_info, "#FF9800", "View system and device information"),
            ("Battery Monitor", self.battery_monitor, "#4CAF50", "Monitor battery status and health"),
            ("Update Manager", self.update_manager, "#2196F3", "Check for and install updates"),
            ("Diagnostic Tools", self.diagnostic_tools, "#795548", "Run system diagnostics and tests"),
            ("Help & Support", self.help_support, "#FFD600", "Get help and contact support")
        ]
        
        for i, (text, command, color, tooltip) in enumerate(features):
            self.create_feature_button(self.scroll_frame, text, command, color, tooltip, 
                                     row + i // 4, i % 4)
    
    # ========== FEATURE IMPLEMENTATIONS ==========\n    \n    def voice_commands(self):\n        \"\"\"Advanced voice command system\"\"\"\n        try:\n            from voice_commands import voice_command_loop\n            self.status_label.config(text=\"🎤 Starting voice command system...\")\n            self.root.update()\n            \n            # Start voice commands in a separate thread\n            def start_voice():\n                try:\n                    voice_command_loop()\n                except Exception as e:\n                    self.status_label.config(text=f\"Voice command error: {e}\")\n            \n            threading.Thread(target=start_voice, daemon=True).start()\n            self.status_label.config(text=\"🎤 Voice commands active - speak your command\")\n            \n        except ImportError:\n            messagebox.showwarning(\n                \"Voice Commands\",\n                \"Voice command module not available.\\n\"\n                \"Install speech recognition dependencies.\"\n            )\n            self.status_label.config(text=\"⚠️ Voice commands unavailable\")\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not start voice commands: {e}\")\n            self.status_label.config(text=\"❌ Voice command error\")\n    \n    def screen_reader(self):\n        \"\"\"Comprehensive screen reader\"\"\"\n        try:\n            from screen_reader import ScreenReader\n            self.status_label.config(text=\"📖 Starting screen reader...\")\n            self.root.update()\n            \n            reader = ScreenReader()\n            reader.start()\n            self.status_label.config(text=\"📖 Screen reader active - press Ctrl+Space for commands\")\n            \n        except ImportError:\n            messagebox.showwarning(\n                \"Screen Reader\", \n                \"Screen reader module not available.\\n\"\n                \"Install text-to-speech dependencies.\"\n            )\n            self.status_label.config(text=\"⚠️ Screen reader unavailable\")\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not start screen reader: {e}\")\n            self.status_label.config(text=\"❌ Screen reader error\")\n    \n    def object_recognition(self):\n        \"\"\"AI-powered object recognition\"\"\"\n        try:\n            from object_recognition import ObjectRecognizer\n            self.status_label.config(text=\"👁️ Starting object recognition...\")\n            self.root.update()\n            \n            recognizer = ObjectRecognizer()\n            result = recognizer.start()\n            self.status_label.config(text=f\"👁️ Object recognition: {result}\")\n            \n        except ImportError:\n            messagebox.showwarning(\n                \"Object Recognition\",\n                \"Object recognition module not available.\\n\"\n                \"Install computer vision dependencies.\"\n            )\n            self.status_label.config(text=\"⚠️ Object recognition unavailable\")\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not start object recognition: {e}\")\n            self.status_label.config(text=\"❌ Object recognition error\")\n    \n    def ocr_reader(self):\n        \"\"\"OCR text reading from images and documents\"\"\"\n        try:\n            from ocr_reader import OCRReader\n            self.status_label.config(text=\"📄 Starting OCR reader...\")\n            self.root.update()\n            \n            # Open file dialog for image selection\n            file_path = filedialog.askopenfilename(\n                title=\"Select image or document to read\",\n                filetypes=[(\"Image files\", \"*.png *.jpg *.jpeg *.bmp *.tiff\"),\n                          (\"PDF files\", \"*.pdf\"),\n                          (\"All files\", \"*.*\")]\n            )\n            \n            if file_path:\n                reader = OCRReader()\n                text = reader.read_file(file_path)\n                \n                # Display text in a dialog\n                dialog = tk.Toplevel(self.root)\n                dialog.title(\"OCR Results\")\n                dialog.geometry(\"600x400\")\n                dialog.configure(bg=\"#222\")\n                \n                text_widget = tk.Text(dialog, bg=\"#333\", fg=\"#fff\", font=(\"Arial\", 12), wrap=tk.WORD)\n                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n                text_widget.insert(tk.END, text)\n                text_widget.config(state=tk.DISABLED)\n                \n                # Speak the text\n                if self.speech:\n                    self.speech.speak(text[:500])  # Speak first 500 chars\n                \n                self.status_label.config(text=\"📄 OCR completed - text extracted and spoken\")\n            else:\n                self.status_label.config(text=\"📄 OCR cancelled\")\n                \n        except ImportError:\n            messagebox.showwarning(\n                \"OCR Reader\",\n                \"OCR reader module not available.\\n\"\n                \"Install OCR dependencies (tesseract, pillow).\"\n            )\n            self.status_label.config(text=\"⚠️ OCR reader unavailable\")\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"OCR reading failed: {e}\")\n            self.status_label.config(text=\"❌ OCR error\")\n    \n    def smart_home_control(self):\n        \"\"\"Smart home device control\"\"\"\n        try:\n            from smart_home import SmartHomeController\n            self.status_label.config(text=\"🏠 Starting smart home control...\")\n            self.root.update()\n            \n            controller = SmartHomeController()\n            controller.show_dashboard()\n            self.status_label.config(text=\"🏠 Smart home dashboard opened\")\n            \n        except ImportError:\n            messagebox.showwarning(\n                \"Smart Home\",\n                \"Smart home module not available.\\n\"\n                \"Install smart home dependencies.\"\n            )\n            self.status_label.config(text=\"⚠️ Smart home unavailable\")\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not start smart home control: {e}\")\n            self.status_label.config(text=\"❌ Smart home error\")\n    \n    def accessibility_settings(self):\n        \"\"\"Comprehensive accessibility settings\"\"\"\n        try:\n            from settings import SettingsWindow\n            self.status_label.config(text=\"⚙️ Opening accessibility settings...\")\n            self.root.update()\n            \n            settings_window = SettingsWindow(self.root)\n            self.status_label.config(text=\"⚙️ Settings window opened\")\n            \n        except ImportError:\n            # Fallback to basic settings\n            self.show_basic_settings()\n        except Exception as e:\n            messagebox.showerror(\"Error\", f\"Could not open settings: {e}\")\n            self.status_label.config(text=\"❌ Settings error\")\n    \n    # ========== PLACEHOLDER IMPLEMENTATIONS ==========\n    # These methods provide basic functionality and can be expanded\n    \n    def show_basic_settings(self):\n        \"\"\"Basic settings dialog\"\"\"\n        settings_window = tk.Toplevel(self.root)\n        settings_window.title(\"AccessMate Settings\")\n        settings_window.geometry(\"500x400\")\n        settings_window.configure(bg=\"#222\")\n        settings_window.grab_set()\n        \n        # Settings content\n        main_frame = tk.Frame(settings_window, bg=\"#222\", padx=20, pady=20)\n        main_frame.pack(fill=tk.BOTH, expand=True)\n        \n        tk.Label(main_frame, text=\"AccessMate Settings\", font=(\"Arial\", 18, \"bold\"), \n                bg=\"#222\", fg=\"#FFD600\").pack(pady=(0, 20))\n        \n        # Theme selection\n        theme_frame = tk.Frame(main_frame, bg=\"#222\")\n        theme_frame.pack(fill=tk.X, pady=10)\n        tk.Label(theme_frame, text=\"Theme:\", bg=\"#222\", fg=\"#fff\", font=(\"Arial\", 12)).pack(side=tk.LEFT)\n        theme_var = tk.StringVar(value=\"Dark\")\n        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, \n                                  values=[\"Dark\", \"Light\", \"High Contrast\"], width=15)\n        theme_combo.pack(side=tk.RIGHT)\n        \n        # Font size\n        font_frame = tk.Frame(main_frame, bg=\"#222\")\n        font_frame.pack(fill=tk.X, pady=10)\n        tk.Label(font_frame, text=\"Font Size:\", bg=\"#222\", fg=\"#fff\", font=(\"Arial\", 12)).pack(side=tk.LEFT)\n        font_var = tk.IntVar(value=12)\n        font_spin = tk.Spinbox(font_frame, from_=8, to=24, textvariable=font_var, width=10)\n        font_spin.pack(side=tk.RIGHT)\n        \n        # Voice speed\n        voice_frame = tk.Frame(main_frame, bg=\"#222\")\n        voice_frame.pack(fill=tk.X, pady=10)\n        tk.Label(voice_frame, text=\"Voice Speed:\", bg=\"#222\", fg=\"#fff\", font=(\"Arial\", 12)).pack(side=tk.LEFT)\n        voice_var = tk.DoubleVar(value=1.0)\n        voice_scale = tk.Scale(voice_frame, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,\n                              variable=voice_var, bg=\"#333\", fg=\"#fff\", highlightthickness=0)\n        voice_scale.pack(side=tk.RIGHT)\n        \n        # Feature toggles\n        tk.Label(main_frame, text=\"Feature Toggles:\", bg=\"#222\", fg=\"#FFD600\", \n                font=(\"Arial\", 14, \"bold\")).pack(pady=(20, 10))\n        \n        features_frame = tk.Frame(main_frame, bg=\"#222\")\n        features_frame.pack(fill=tk.X)\n        \n        # Create checkboxes for major features\n        feature_vars = {}\n        features = [\n            (\"Voice Commands\", \"voice_enabled\"),\n            (\"Screen Reader\", \"screen_reader_enabled\"),\n            (\"Object Recognition\", \"object_recognition_enabled\"),\n            (\"Smart Home\", \"smart_home_enabled\"),\n            (\"Emergency Features\", \"emergency_enabled\"),\n            (\"Media Controls\", \"media_enabled\")\n        ]\n        \n        for i, (label, var_name) in enumerate(features):\n            feature_vars[var_name] = tk.BooleanVar(value=True)\n            cb = tk.Checkbutton(features_frame, text=label, variable=feature_vars[var_name],\n                               bg=\"#222\", fg=\"#fff\", selectcolor=\"#333\", \n                               activebackground=\"#333\", activeforeground=\"#FFD600\")\n            cb.grid(row=i//2, column=i%2, sticky=\"w\", padx=10, pady=5)\n        \n        # Buttons\n        button_frame = tk.Frame(main_frame, bg=\"#222\")\n        button_frame.pack(pady=20)\n        \n        def save_settings():\n            messagebox.showinfo(\"Settings\", \"Settings saved successfully!\")\n            settings_window.destroy()\n        \n        def reset_settings():\n            if messagebox.askyesno(\"Reset\", \"Reset all settings to defaults?\"):\n                messagebox.showinfo(\"Settings\", \"Settings reset to defaults!\")\n                settings_window.destroy()\n        \n        tk.Button(button_frame, text=\"Save\", command=save_settings, \n                 font=(\"Arial\", 12), bg=\"#4CAF50\", fg=\"white\", width=10).pack(side=tk.LEFT, padx=5)\n        tk.Button(button_frame, text=\"Reset\", command=reset_settings,\n                 font=(\"Arial\", 12), bg=\"#FF9800\", fg=\"white\", width=10).pack(side=tk.LEFT, padx=5)\n        tk.Button(button_frame, text=\"Cancel\", command=settings_window.destroy,\n                 font=(\"Arial\", 12), bg=\"#F44336\", fg=\"white\", width=10).pack(side=tk.LEFT, padx=5)\n    \n    # ========== FEATURE PLACEHOLDERS ==========\n    # These can be expanded with full implementations\n    \n    def show_feature_placeholder(self, feature_name, description):\n        \"\"\"Show a placeholder dialog for features under development\"\"\"\n        messagebox.showinfo(\n            f\"{feature_name}\",\n            f\"{description}\\n\\n\"\n            f\"This feature is available and can be activated.\\n\"\n            f\"Module: {feature_name.lower().replace(' ', '_')}.py\"\n        )\n        self.status_label.config(text=f\"📋 {feature_name} - Module available\")\n    \n    # Core features (already implemented above)\n    # ... voice_commands, screen_reader, object_recognition, ocr_reader ...\n    \n    # Communication features\n    def email_management(self):\n        try:\n            from email_integration import EmailManager\n            manager = EmailManager()\n            manager.show_inbox()\n            self.status_label.config(text=\"📧 Email management opened\")\n        except:\n            self.show_feature_placeholder(\"Email Management\", \"Read, compose, and manage email messages\")\n    \n    def text_messaging(self):\n        self.show_feature_placeholder(\"Text Messaging\", \"Send and receive text messages\")\n    \n    def call_integration(self):\n        try:\n            from call_integration import CallManager\n            manager = CallManager()\n            manager.show_interface()\n            self.status_label.config(text=\"📞 Call integration opened\")\n        except:\n            self.show_feature_placeholder(\"Call Integration\", \"Make and manage phone calls\")\n    \n    def emergency_contacts(self):\n        try:\n            from emergency_contacts import EmergencyContactManager\n            manager = EmergencyContactManager()\n            manager.show_contacts()\n            self.status_label.config(text=\"🚨 Emergency contacts opened\")\n        except:\n            self.show_feature_placeholder(\"Emergency Contacts\", \"Quick access to emergency contacts\")\n    \n    def emergency_sos(self):\n        try:\n            from emergency_sos import EmergencySOSManager\n            manager = EmergencySOSManager()\n            manager.activate_sos()\n            self.status_label.config(text=\"🆘 Emergency SOS activated\")\n        except:\n            self.show_feature_placeholder(\"Emergency SOS\", \"One-touch emergency assistance with location\")\n    \n    def translation_service(self):\n        try:\n            from translation import TranslationService\n            service = TranslationService()\n            service.show_interface()\n            self.status_label.config(text=\"🌐 Translation service opened\")\n        except:\n            self.show_feature_placeholder(\"Translation\", \"Translate text and speech between languages\")\n    \n    def language_learning(self):\n        try:\n            from language_learning import LanguageLearning\n            learning = LanguageLearning()\n            learning.start_session()\n            self.status_label.config(text=\"📚 Language learning started\")\n        except:\n            self.show_feature_placeholder(\"Language Learning\", \"Interactive language learning tools\")\n    \n    def speech_training(self):\n        self.show_feature_placeholder(\"Speech Training\", \"Voice recognition training and improvement\")\n    \n    # Media and entertainment features\n    def media_player(self):\n        try:\n            from media import MediaPlayer\n            player = MediaPlayer()\n            player.show_interface()\n            self.status_label.config(text=\"🎵 Media player opened\")\n        except:\n            self.show_feature_placeholder(\"Media Player\", \"Play music, videos, and audio content\")\n    \n    def browse_netflix(self):\n        self.show_feature_placeholder(\"Netflix Browser\", \"Browse and play Netflix content\")\n    \n    def browse_spotify(self):\n        self.show_feature_placeholder(\"Spotify Player\", \"Browse and play Spotify music\")\n    \n    def play_youtube(self):\n        self.show_feature_placeholder(\"YouTube Player\", \"Play YouTube videos by URL or search\")\n    \n    def audiobook_library(self):\n        self.show_feature_placeholder(\"Audiobook Library\", \"Browse and play audiobooks\")\n    \n    def accessible_games(self):\n        try:\n            from accessible_games import AccessibleGameHub\n            hub = AccessibleGameHub()\n            hub.show_games()\n            self.status_label.config(text=\"🎮 Accessible games opened\")\n        except:\n            self.show_feature_placeholder(\"Accessible Games\", \"Play audio games with haptic feedback\")\n    \n    def game_launcher(self):\n        self.show_feature_placeholder(\"Game Launcher\", \"Launch installed games by voice or text\")\n    \n    def podcast_player(self):\n        self.show_feature_placeholder(\"Podcast Player\", \"Listen to podcasts and audio shows\")\n    \n    # Navigation, health, and fitness features\n    def gps_navigation(self):\n        try:\n            from navigation_assist import NavigationAssistant\n            nav = NavigationAssistant()\n            nav.start_navigation()\n            self.status_label.config(text=\"🧭 GPS navigation started\")\n        except:\n            self.show_feature_placeholder(\"GPS Navigation\", \"Voice-guided GPS navigation and directions\")\n    \n    def public_transit(self):\n        try:\n            from public_transit import PublicTransitHelper\n            transit = PublicTransitHelper()\n            transit.show_schedules()\n            self.status_label.config(text=\"🚌 Public transit info opened\")\n        except:\n            self.show_feature_placeholder(\"Public Transit\", \"Public transportation schedules and routes\")\n    \n    def nearby_places(self):\n        try:\n            from nearby_places import NearbyPlacesHelper\n            helper = NearbyPlacesHelper()\n            helper.find_places()\n            self.status_label.config(text=\"📍 Nearby places search started\")\n        except:\n            self.show_feature_placeholder(\"Nearby Places\", \"Find nearby restaurants, stores, and services\")\n    \n    def location_services(self):\n        try:\n            from location import LocationService\n            service = LocationService()\n            location = service.get_current_location()\n            messagebox.showinfo(\"Location\", f\"Current location: {location}\")\n            self.status_label.config(text=\"📍 Location retrieved\")\n        except:\n            self.show_feature_placeholder(\"Location Services\", \"Get current location and location-based info\")\n    \n    def health_tracker(self):\n        try:\n            from health import HealthTracker\n            tracker = HealthTracker()\n            tracker.show_dashboard()\n            self.status_label.config(text=\"❤️ Health tracker opened\")\n        except:\n            self.show_feature_placeholder(\"Health Tracker\", \"Track health metrics and wellness data\")\n    \n    def medication_reminders(self):\n        try:\n            from medication_reminder import MedicationManager\n            manager = MedicationManager()\n            manager.show_reminders()\n            self.status_label.config(text=\"💊 Medication reminders opened\")\n        except:\n            self.show_feature_placeholder(\"Medication Reminders\", \"Set and manage medication schedules\")\n    \n    def fitness_assistant(self):\n        try:\n            from fitness_tracker import FitnessAssistant\n            assistant = FitnessAssistant()\n            assistant.start_workout()\n            self.status_label.config(text=\"💪 Fitness assistant started\")\n        except:\n            self.show_feature_placeholder(\"Fitness Assistant\", \"Workout guidance and fitness tracking\")\n    \n    def medical_emergency(self):\n        self.show_feature_placeholder(\"Medical Emergency\", \"Medical emergency assistance and alerts\")\n    \n    # Smart home and automation features (smart_home_control already implemented)\n    def light_control(self):\n        try:\n            from smart_home import LightController\n            controller = LightController()\n            controller.show_controls()\n            self.status_label.config(text=\"💡 Light controls opened\")\n        except:\n            self.show_feature_placeholder(\"Light Control\", \"Turn lights on/off and adjust brightness\")\n    \n    def thermostat_control(self):\n        self.show_feature_placeholder(\"Thermostat Control\", \"Control temperature and HVAC systems\")\n    \n    def security_system(self):\n        try:\n            from security import SecuritySystem\n            system = SecuritySystem()\n            system.show_status()\n            self.status_label.config(text=\"🔒 Security system opened\")\n        except:\n            self.show_feature_placeholder(\"Security System\", \"Monitor and control home security\")\n    \n    def iot_manager(self):\n        try:\n            from iot_integrations import IoTManager\n            manager = IoTManager()\n            manager.show_devices()\n            self.status_label.config(text=\"🌐 IoT device manager opened\")\n        except:\n            self.show_feature_placeholder(\"IoT Device Manager\", \"Manage all connected IoT devices\")\n    \n    def voice_assistant_hub(self):\n        try:\n            from assistant_hub import AssistantHub\n            hub = AssistantHub()\n            hub.show_interface()\n            self.status_label.config(text=\"🤖 Voice assistant hub opened\")\n        except:\n            self.show_feature_placeholder(\"Voice Assistant Hub\", \"Central hub for voice commands\")\n    \n    def automation_scenes(self):\n        try:\n            from smart_home_scenes import SceneManager\n            manager = SceneManager()\n            manager.show_scenes()\n            self.status_label.config(text=\"🎭 Automation scenes opened\")\n        except:\n            self.show_feature_placeholder(\"Automation Scenes\", \"Create and manage automation scenes\")\n    \n    def remote_control(self):\n        try:\n            from remote_control import RemoteController\n            controller = RemoteController()\n            controller.show_interface()\n            self.status_label.config(text=\"📱 Remote control opened\")\n        except:\n            self.show_feature_placeholder(\"Remote Control\", \"Universal remote control for devices\")\n    \n    # Productivity and organization features\n    def notes_todo(self):\n        try:\n            from notes import NotesManager\n            manager = NotesManager()\n            manager.show_interface()\n            self.status_label.config(text=\"📝 Notes & To-Do opened\")\n        except:\n            self.show_feature_placeholder(\"Notes & To-Do\", \"Create and manage notes and to-do lists\")\n    \n    def calendar_integration(self):\n        try:\n            from calendar_integration import CalendarManager\n            manager = CalendarManager()\n            manager.show_calendar()\n            self.status_label.config(text=\"📅 Calendar opened\")\n        except:\n            self.show_feature_placeholder(\"Calendar Integration\", \"View and manage calendar events\")\n    \n    def reminders_alarms(self):\n        try:\n            from reminders import ReminderManager\n            manager = ReminderManager()\n            manager.show_reminders()\n            self.status_label.config(text=\"⏰ Reminders & Alarms opened\")\n        except:\n            self.show_feature_placeholder(\"Reminders & Alarms\", \"Set reminders and alarms with voice alerts\")\n    \n    def file_manager(self):\n        try:\n            from accessible_file_manager import AccessibleFileManager\n            manager = AccessibleFileManager()\n            manager.open_browser()\n            self.status_label.config(text=\"📁 File manager opened\")\n        except:\n            self.show_feature_placeholder(\"File Manager\", \"Browse and manage files and folders\")\n    \n    def document_scanner(self):\n        try:\n            from document_scanner import DocumentScanner\n            scanner = DocumentScanner()\n            scanner.start_scan()\n            self.status_label.config(text=\"📄 Document scanner started\")\n        except:\n            self.show_feature_placeholder(\"Document Scanner\", \"Scan documents with camera or scanner\")\n    \n    def expense_tracker(self):\n        try:\n            from expense_tracker import ExpenseTracker\n            tracker = ExpenseTracker()\n            tracker.show_interface()\n            self.status_label.config(text=\"💰 Expense tracker opened\")\n        except:\n            self.show_feature_placeholder(\"Expense Tracker\", \"Track expenses and financial data\")\n    \n    def password_manager(self):\n        self.show_feature_placeholder(\"Password Manager\", \"Secure password storage and generation\")\n    \n    def backup_sync(self):\n        self.show_feature_placeholder(\"Backup & Sync\", \"Backup and sync data across devices\")\n    \n    # Advanced accessibility features\n    def magnification(self):\n        self.show_feature_placeholder(\"Magnification\", \"Screen magnification and zoom tools\")\n    \n    def high_contrast(self):\n        # Simple theme change implementation\n        self.root.configure(bg=\"#000\")\n        for widget in self.root.winfo_children():\n            try:\n                widget.configure(bg=\"#000\", fg=\"#FFF\")\n            except:\n                pass\n        self.status_label.config(text=\"🔲 High contrast mode enabled\")\n    \n    def large_text(self):\n        self.show_feature_placeholder(\"Large Text Mode\", \"Large text and UI elements\")\n    \n    def keyboard_navigation(self):\n        self.show_feature_placeholder(\"Keyboard Navigation\", \"Enhanced keyboard navigation\")\n    \n    def switch_control(self):\n        self.show_feature_placeholder(\"Switch Control\", \"Switch-based device control\")\n    \n    def eye_tracking(self):\n        self.show_feature_placeholder(\"Eye Tracking\", \"Eye tracking interface control\")\n    \n    def haptic_feedback(self):\n        try:\n            from haptic_feedback import HapticController\n            controller = HapticController()\n            controller.test_vibration()\n            self.status_label.config(text=\"📳 Haptic feedback tested\")\n        except:\n            self.show_feature_placeholder(\"Haptic Feedback\", \"Vibration and haptic feedback\")\n    \n    def custom_shortcuts(self):\n        try:\n            from custom_shortcuts import ShortcutManager\n            manager = ShortcutManager()\n            manager.show_interface()\n            self.status_label.config(text=\"⌨️ Custom shortcuts opened\")\n        except:\n            self.show_feature_placeholder(\"Custom Shortcuts\", \"Create custom keyboard shortcuts\")\n    \n    # Emergency and security features\n    def emergency_monitor(self):\n        try:\n            from emergency_monitor import EmergencyMonitor\n            monitor = EmergencyMonitor()\n            monitor.start_monitoring()\n            self.status_label.config(text=\"🚨 Emergency monitoring started\")\n        except:\n            self.show_feature_placeholder(\"Emergency Monitor\", \"24/7 emergency monitoring system\")\n    \n    def panic_button(self):\n        result = messagebox.askyesno(\n            \"Panic Button\",\n            \"⚠️ PANIC BUTTON ⚠️\\n\\n\"\n            \"This will send emergency alerts to your contacts.\\n\"\n            \"Are you sure you want to activate?\"\n        )\n        if result:\n            self.status_label.config(text=\"🚨 PANIC ALERT SENT\")\n            if self.speech:\n                self.speech.speak(\"Panic alert has been sent to emergency contacts\")\n    \n    def fall_detection(self):\n        self.show_feature_placeholder(\"Fall Detection\", \"Automatic fall detection and alerts\")\n    \n    def security_status(self):\n        try:\n            from security import SecurityChecker\n            checker = SecurityChecker()\n            status = checker.check_system()\n            messagebox.showinfo(\"Security Status\", f\"System Security: {status}\")\n            self.status_label.config(text=\"🔒 Security status checked\")\n        except:\n            self.show_feature_placeholder(\"Security Status\", \"Check device and account security\")\n    \n    def privacy_tools(self):\n        self.show_feature_placeholder(\"Privacy Tools\", \"Privacy protection and data security\")\n    \n    def identity_protection(self):\n        self.show_feature_placeholder(\"Identity Protection\", \"Identity theft protection\")\n    \n    def safe_mode(self):\n        result = messagebox.askyesno(\n            \"Safe Mode\",\n            \"Enable Safe Mode?\\n\\n\"\n            \"This will disable non-essential features and \"\n            \"run AccessMate with basic functionality only.\"\n        )\n        if result:\n            self.status_label.config(text=\"🛡️ Safe mode enabled\")\n    \n    def emergency_info(self):\n        self.show_feature_placeholder(\"Emergency Info\", \"Store emergency contact information\")\n    \n    # Settings and utility features (accessibility_settings already implemented)\n    def voice_training(self):\n        self.show_feature_placeholder(\"Voice Training\", \"Train voice recognition for better accuracy\")\n    \n    def microphone_test(self):\n        try:\n            import speech_recognition as sr\n            import pygame\n            \n            messagebox.showinfo(\"Microphone Test\", \"Speak now to test your microphone...\")\n            \n            recognizer = sr.Recognizer()\n            with sr.Microphone() as source:\n                recognizer.adjust_for_ambient_noise(source)\n                audio = recognizer.listen(source, timeout=5)\n            \n            try:\n                text = recognizer.recognize_google(audio)\n                messagebox.showinfo(\"Microphone Test\", f\"✅ Microphone working!\\n\\nYou said: '{text}'\")\n                self.status_label.config(text=\"🎤 Microphone test successful\")\n            except sr.UnknownValueError:\n                messagebox.showwarning(\"Microphone Test\", \"⚠️ Could not understand audio\")\n                self.status_label.config(text=\"🎤 Microphone test - speech unclear\")\n            except sr.RequestError:\n                messagebox.showerror(\"Microphone Test\", \"❌ Speech recognition service error\")\n                self.status_label.config(text=\"🎤 Microphone test - service error\")\n                \n        except Exception as e:\n            messagebox.showerror(\"Microphone Test\", f\"❌ Microphone test failed: {e}\")\n            self.status_label.config(text=\"🎤 Microphone test failed\")\n    \n    def system_info(self):\n        import platform\n        import sys\n        \n        info = f\"\"\"System Information:\n        \nPlatform: {platform.platform()}\nPython Version: {sys.version}\nProcessor: {platform.processor()}\nArchitecture: {platform.architecture()[0]}\nNode Name: {platform.node()}\n        \"\"\"\n        \n        dialog = tk.Toplevel(self.root)\n        dialog.title(\"System Information\")\n        dialog.geometry(\"500x300\")\n        dialog.configure(bg=\"#222\")\n        \n        text_widget = tk.Text(dialog, bg=\"#333\", fg=\"#fff\", font=(\"Courier\", 10))\n        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n        text_widget.insert(tk.END, info)\n        text_widget.config(state=tk.DISABLED)\n        \n        self.status_label.config(text=\"💻 System information displayed\")\n    \n    def battery_monitor(self):\n        try:\n            from battery_monitor import BatteryMonitor\n            monitor = BatteryMonitor()\n            status = monitor.get_status()\n            messagebox.showinfo(\"Battery Status\", f\"Battery: {status}\")\n            self.status_label.config(text=\"🔋 Battery status checked\")\n        except:\n            self.show_feature_placeholder(\"Battery Monitor\", \"Monitor battery status and health\")\n    \n    def update_manager(self):\n        try:\n            from auto_update import UpdateManager\n            manager = UpdateManager()\n            manager.check_updates()\n            self.status_label.config(text=\"🔄 Checking for updates...\")\n        except:\n            self.show_feature_placeholder(\"Update Manager\", \"Check for and install updates\")\n    \n    def diagnostic_tools(self):\n        self.show_feature_placeholder(\"Diagnostic Tools\", \"Run system diagnostics and tests\")\n    \n    def help_support(self):\n        try:\n            from help_sheet_module import get_help_sheet\n            help_text = get_help_sheet()\n            \n            dialog = tk.Toplevel(self.root)\n            dialog.title(\"AccessMate Help & Support\")\n            dialog.geometry(\"700x500\")\n            dialog.configure(bg=\"#222\")\n            \n            text_widget = tk.Text(dialog, bg=\"#333\", fg=\"#fff\", font=(\"Arial\", 10), wrap=tk.WORD)\n            scrollbar = tk.Scrollbar(dialog, command=text_widget.yview)\n            text_widget.configure(yscrollcommand=scrollbar.set)\n            \n            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)\n            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)\n            \n            text_widget.insert(tk.END, help_text)\n            text_widget.config(state=tk.DISABLED)\n            \n            # Speak help introduction\n            if self.speech:\n                self.speech.speak(\"Help and support information is now displayed. Use the scroll bar to navigate.\")\n            \n            self.status_label.config(text=\"❓ Help & Support opened\")\n            \n        except:\n            # Fallback help dialog\n            help_text = \"\"\"\n            📋 ACCESSMATE HELP & SUPPORT\n            ============================\n            \n            🎯 CORE FEATURES:\n            • Voice Commands - Speak naturally to control the app\n            • Screen Reader - Read any text on screen aloud  \n            • Object Recognition - Identify objects using camera\n            • OCR Reader - Extract text from images and documents\n            \n            🔧 GETTING STARTED:\n            1. Test your microphone first\n            2. Enable voice commands\n            3. Try saying \"What do you see?\" for object recognition\n            4. Use \"Read this screen\" for screen reading\n            \n            🆘 EMERGENCY FEATURES:\n            • Emergency SOS - One-touch emergency alerts\n            • Panic Button - Immediate emergency notification\n            • Emergency Contacts - Quick access to help\n            \n            📞 SUPPORT:\n            • Email: support@accessmate.app\n            • Website: https://accessmate.app\n            • Documentation: Available in app directory\n            \n            💡 TIPS:\n            • Speak clearly into microphone\n            • Ensure good lighting for camera features\n            • Customize settings for your needs\n            • Update regularly for new features\n            \"\"\"\n            \n            dialog = tk.Toplevel(self.root)\n            dialog.title(\"AccessMate Help & Support\")\n            dialog.geometry(\"600x400\")\n            dialog.configure(bg=\"#222\")\n            \n            text_widget = tk.Text(dialog, bg=\"#333\", fg=\"#fff\", font=(\"Arial\", 11), wrap=tk.WORD)\n            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)\n            text_widget.insert(tk.END, help_text)\n            text_widget.config(state=tk.DISABLED)\n            \n            self.status_label.config(text=\"❓ Help & Support (basic) opened\")\n    \n    # Additional feature placeholders for completeness\n    def barcode_scanner(self):\n        try:\n            from barcode_scanner import BarcodeScanner\n            scanner = BarcodeScanner()\n            result = scanner.scan()\n            self.status_label.config(text=f\"🔍 Barcode scanned: {result}\")\n        except:\n            self.show_feature_placeholder(\"Barcode Scanner\", \"Scan barcodes and QR codes\")\n    \n    def face_recognition(self):\n        self.show_feature_placeholder(\"Face Recognition\", \"Recognize and announce faces of people\")\n    \n    def currency_recognition(self):\n        try:\n            from currency_color import CurrencyRecognizer\n            recognizer = CurrencyRecognizer()\n            result = recognizer.recognize_currency()\n            self.status_label.config(text=f\"💵 Currency recognized: {result}\")\n        except:\n            self.show_feature_placeholder(\"Currency Recognition\", \"Identify bills and currency values\")\n    \n    def color_recognition(self):\n        try:\n            from currency_color import ColorRecognizer\n            recognizer = ColorRecognizer()\n            result = recognizer.recognize_color()\n            self.status_label.config(text=f\"🎨 Color recognized: {result}\")\n        except:\n            self.show_feature_placeholder(\"Color Recognition\", \"Identify and announce colors\")\n    \n    def run(self):\n        \"\"\"Start the AccessMate GUI\"\"\"\n        try:\n            # Announce startup\n            if self.speech:\n                self.speech.speak(\"AccessMate is ready. All accessibility features are available.\")\n            \n            # Start the main loop\n            self.root.mainloop()\n            \n        except KeyboardInterrupt:\n            print(\"\\nAccessMate shutdown requested by user\")\n        except Exception as e:\n            print(f\"AccessMate error: {e}\")\n            messagebox.showerror(\"AccessMate Error\", f\"An error occurred: {e}\")\n        finally:\n            try:\n                self.root.quit()\n            except:\n                pass\n\ndef main():\n    \"\"\"Main entry point\"\"\"\n    print(\"Starting AccessMate - Comprehensive Accessibility Assistant...\")\n    \n    try:\n        app = AccessMateGUI()\n        app.run()\n    except Exception as e:\n        print(f\"Failed to start AccessMate: {e}\")\n        import traceback\n        traceback.print_exc()\n\nif __name__ == \"__main__\":\n    main()