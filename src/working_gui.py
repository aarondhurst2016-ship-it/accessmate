# GUI module for AccessMate

import tkinter as tk
from tkinter import ttk
from accessibility import enable_accessibility, setup_accessibility_shortcuts
import speech
from speech import speak, say_time, say_date, say_weather
from help_sheet import get_help_sheet

THEMES = {
    "Dark": {"bg": "#222", "fg": "#fff", "btn_bg": "#333", "btn_fg": "#FFD600"},
    "Light": {"bg": "#fff", "fg": "#222", "btn_bg": "#eee", "btn_fg": "#222"},
    "Blue": {"bg": "#1976D2", "fg": "#fff", "btn_bg": "#2196F3", "btn_fg": "#FFD600"}
}


from ocr_screen_reader import get_ultra_low_power_mode, set_ultra_low_power_mode

def launch(gui_instance=None):
    import sys
    def set_startup(enable=True):
        if sys.platform.startswith('win'):
            import winreg
            exe_path = os.path.abspath(sys.argv[0])
            app_name = "AccessMateWin"
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as regkey:
                if enable:
                    winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(regkey, app_name)
                    except FileNotFoundError:
                        pass
            return True
        return False

    import traceback
    LOGFILE = os.path.expanduser("~/.accessmate_error.log")
    def log_error(e):
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"\n---\n{traceback.format_exc()}\n")
        content_var.set("An error occurred. Details have been logged.")
        speak("An error occurred. Please check the log file or contact support.")
    import os
    from settings import Settings
    user_settings = Settings()
    user_settings.load("user_settings.json")

    # Onboarding: show on first run
    onboarding_file = os.path.expanduser("~/.accessmate_onboarded")
    def show_onboarding():
        onboarding_text = (
            "Welcome to AccessMate!\n\n"
            "This app is designed for accessibility.\n"
            "- Use the feature buttons or voice commands.\n"
            "- You can turn features on or off in Settings.\n"
            "- Press 'Help' for a list of commands.\n"
            "- All actions are accessible by keyboard and screen reader.\n\n"
            "For a full tutorial, press the 'Tutorial' button."
        )
        content_var.set(onboarding_text)
        speak(onboarding_text)

    if not os.path.exists(onboarding_file):
        show_onboarding()
        with open(onboarding_file, "w") as f:
            f.write("onboarded\n")

    def show_tutorial():
        tutorial_text = (
            "TUTORIAL:\n"
            "1. Use the microphone button or say 'Voice Command' to control the app by voice.\n"
            "2. Use the feature buttons to access OCR, reminders, games, and more.\n"
            "3. Go to Settings to enable or disable features.\n"
            "4. Press 'Help' for a list of all commands.\n"
            "5. For support, see the README or contact support.\n"
        )
        content_var.set(tutorial_text)
        speak(tutorial_text)

    """Main GUI launch function"""
    root = tk.Tk()
    root.title("AccessMate")
    root.geometry("1000x800")
    root.configure(bg="#222")

    # Create scrollable canvas
    canvas = tk.Canvas(root, bg="#222", highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#222")
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    # Content display
    content_var = tk.StringVar(value="Welcome to AccessMate!")
    content_label = tk.Label(scroll_frame, textvariable=content_var, font=("Arial", 16), bg="#222", fg="#fff", wraplength=900)
    content_label.grid(row=0, column=0, columnspan=3, pady=10)

    # Ultra-low-power mode toggle
    ulp_status = tk.StringVar()
    def update_ulp_status():
        ulp_status.set(f"Ultra Low Power Mode: {get_ultra_low_power_mode()}")
    def ulp_on():
        set_ultra_low_power_mode(True)
        update_ulp_status()
        content_var.set("Ultra Low Power Mode enabled.")
    def ulp_off():
        set_ultra_low_power_mode(False)
        update_ulp_status()
        content_var.set("Ultra Low Power Mode disabled.")
    def ulp_auto():
        set_ultra_low_power_mode(None)
        update_ulp_status()
        content_var.set("Ultra Low Power Mode set to auto.")
    update_ulp_status()
    tk.Label(scroll_frame, textvariable=ulp_status, font=("Arial", 14), bg="#222", fg="#FFD600").grid(row=2, column=0, columnspan=2, pady=8, sticky="w")
    tk.Button(scroll_frame, text="Low Power: On", command=ulp_on, font=("Arial", 12), bg="#333", fg="#FFD600").grid(row=2, column=2, padx=4, pady=8)
    tk.Button(scroll_frame, text="Low Power: Off", command=ulp_off, font=("Arial", 12), bg="#333", fg="#FFD600").grid(row=2, column=3, padx=4, pady=8)
    tk.Button(scroll_frame, text="Low Power: Auto", command=ulp_auto, font=("Arial", 12), bg="#333", fg="#FFD600").grid(row=2, column=4, padx=4, pady=8)

    # Microphone selection
    mic_names = speech.list_microphones()
    mic_var = tk.StringVar(value=mic_names[0] if mic_names else "Default")
    
    def set_mic(event=None):
        try:
            idx = mic_names.index(mic_var.get()) if mic_var.get() in mic_names else 0
            speech.selected_mic_index = idx
            content_var.set(f"Microphone selected: {mic_var.get()} (index {idx})")
            speak(f"Microphone selected: {mic_var.get()}")
        except Exception as e:
            content_var.set("Microphone selection failed")
            print(f"Microphone error: {e}")
    
    mic_label = tk.Label(scroll_frame, text="Select Microphone:", font=("Arial", 16), bg="#222", fg="#FFD600")
    mic_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    mic_combo = ttk.Combobox(scroll_frame, textvariable=mic_var, values=mic_names, font=("Arial", 16), width=30)
    mic_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    mic_combo.bind("<<ComboboxSelected>>", set_mic)
    enable_accessibility(mic_combo, tooltip="Choose which microphone to use for speech input.")

    # Theme selection
    current_theme = tk.StringVar(value="Dark")
    
    def apply_theme(theme_name):
        theme = THEMES.get(theme_name, THEMES["Dark"])
        root.configure(bg=theme["bg"])
        canvas.configure(bg=theme["bg"])
        scroll_frame.configure(bg=theme["bg"])
        content_label.configure(bg=theme["bg"], fg=theme["fg"])
        mic_label.configure(bg=theme["bg"], fg=theme["fg"])

    theme_label = tk.Label(scroll_frame, text="Theme:", font=("Arial", 16), bg="#222", fg="#FFD600")
    theme_label.grid(row=0, column=3, padx=10, pady=10, sticky="w")
    theme_combo = ttk.Combobox(scroll_frame, textvariable=current_theme, values=list(THEMES.keys()), font=("Arial", 16), width=18)
    theme_combo.grid(row=0, column=4, padx=10, pady=10, sticky="w")
    theme_combo.bind("<<ComboboxSelected>>", lambda e: apply_theme(current_theme.get()))
    apply_theme(current_theme.get())

    # Test microphone function
    def test_microphone():
        try:
            import speech_recognition as sr
            import pygame
            import tempfile, os
            recognizer = sr.Recognizer()
            
            mic_index = getattr(speech, 'selected_mic_index', None)
            if mic_index is None:
                source = sr.Microphone()
            else:
                source = sr.Microphone(device_index=mic_index)
                
            with source as src:
                content_var.set("Recording... Please speak.")
                root.update()
                audio = recognizer.listen(src, timeout=5)
                content_var.set("Playing back your recording...")
                root.update()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf:
                    temp_filename = tf.name
                with open(temp_filename, "wb") as f:
                    f.write(audio.get_wav_data())
                    
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                
                try:
                    os.remove(temp_filename)
                except PermissionError:
                    pass
                    
                content_var.set("Mic test complete.")
        except Exception as e:
            log_error(e)

    # Feature buttons
    def toggle_startup_gui():
        if sys.platform.startswith('win'):
            enabled = getattr(user_settings, 'startup_enabled', False)
            new_state = not enabled
            if set_startup(new_state):
                user_settings.startup_enabled = new_state
                user_settings.save("user_settings.json")
                msg = "Startup enabled." if new_state else "Startup disabled."
                content_var.set(msg)
                speak(msg)
            else:
                content_var.set("Startup option only available on Windows.")
                speak("Startup option only available on Windows.")
        else:
            content_var.set("Startup option only available on Windows.")
            speak("Startup option only available on Windows.")

    feature_buttons = [
        ("Test Microphone", "#FF9800", "Record and play back your voice to test the mic.", test_microphone),
        ("Help", "#FFD600", "Show help sheet and speak instructions.", lambda: (content_var.set(get_help_sheet()), speak(get_help_sheet()))),
        ("Tutorial", "#00B8D4", "Show a step-by-step tutorial for new users.", show_tutorial),
        ("Say Time", "#4CAF50", "Speak the current time.", lambda: say_time()),
        ("Say Date", "#009688", "Speak today's date.", lambda: say_date()),
        ("Say Weather", "#1976D2", "Speak the weather.", lambda: say_weather()),
    ("Settings", "#4FC3F7", "Open app settings.", lambda: content_var.set("Settings feature coming soon.")),
    ("Toggle Startup", "#607D8B", "Enable or disable auto-start on Windows login.", toggle_startup_gui),
        ("Reminders & Alarms", "#FFB300", "Set reminders and alarms.", lambda: content_var.set("Reminders feature coming soon.")),
        ("Calendar", "#7CB342", "View and sync calendar.", lambda: content_var.set("Calendar feature coming soon.")),
        ("Notes & To-Do", "#039BE5", "Take notes and manage to-dos.", lambda: content_var.set("Notes feature coming soon.")),
        ("Email", "#E91E63", "Send and receive emails.", lambda: content_var.set("Email feature coming soon.")),
        ("Smart Home", "#8BC34A", "Control smart home devices.", lambda: content_var.set("Smart Home feature coming soon.")),
        ("File Manager", "#388E3C", "Manage your files.", lambda: content_var.set("File Manager feature coming soon.")),
        ("Media", "#7E57C2", "Play and manage media.", lambda: content_var.set("Media feature coming soon.")),
        ("Location", "#0097A7", "Get location info.", lambda: content_var.set("Location feature coming soon.")),
        ("Translation", "#3949AB", "Translate text and speech.", lambda: content_var.set("Translation feature coming soon.")),
        ("Health", "#D32F2F", "Track health and fitness.", lambda: content_var.set("Health feature coming soon.")),
        ("Security", "#E53935", "Security and privacy controls.", lambda: content_var.set("Security feature coming soon.")),
        ("Dashboard", "#FFA726", "View dashboard and stats.", lambda: content_var.set("Dashboard feature coming soon.")),
    ]

    def make_on_enter(tip, widget):
        def on_enter(event):
            text = tip or widget.cget('text')
            try:
                speak(text)
            except Exception as e:
                log_error(e)
        return on_enter

    # Create feature buttons
    for i, (label, color, tooltip, cmd) in enumerate(feature_buttons):
        btn = tk.Button(scroll_frame, text=label, command=cmd, font=("Arial", 18), bg=color, fg="white", width=22, height=2)
        btn.grid(row=2 + i // 3, column=i % 3, padx=10, pady=10)
        enable_accessibility(btn, tooltip=tooltip)
        btn.bind('<Enter>', make_on_enter(tooltip, btn))

    # Set up accessibility shortcuts
    setup_accessibility_shortcuts(root)
    
    # Welcome message
    try:
        speak("Welcome to AccessMate!")
    except Exception as e:
        log_error(e)
    
    try:
        root.mainloop()
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    launch(None)