# Speech module for Talkback Assistant
import pyttsx3
import speech_recognition as sr
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading

# Global variables
selected_mic_index = None
tts_engine = None

def init_tts():
    """Initialize text-to-speech engine"""
    global tts_engine
    try:
        tts_engine = pyttsx3.init()
        # Set properties
        voices = tts_engine.getProperty('voices')
        if voices:
            tts_engine.setProperty('voice', voices[0].id)  # Use first available voice
        tts_engine.setProperty('rate', 150)  # Speech rate
        tts_engine.setProperty('volume', 0.9)  # Volume level
        return True
    except Exception as e:
        print(f"TTS initialization failed: {e}")
        return False

def speak(text):
    """Convert text to speech"""
    global tts_engine
    if tts_engine is None:
        init_tts()
    
    if tts_engine:
        try:
            def _speak():
                tts_engine.say(text)
                tts_engine.runAndWait()
            
            # Run TTS in a separate thread to avoid blocking
            thread = threading.Thread(target=_speak)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Speech failed: {e}")
    else:
        print(f"TTS not available. Would say: {text}")

def list_microphones():
    """Get list of available microphones"""
    try:
        mic_list = sr.Microphone.list_microphone_names()
        return mic_list if mic_list else ["Default Microphone"]
    except Exception as e:
        print(f"Error listing microphones: {e}")
        return ["Default Microphone"]

def listen_for_speech(timeout=5):
    """Listen for speech input and return recognized text"""
    recognizer = sr.Recognizer()
    
    try:
        if selected_mic_index is not None:
            microphone = sr.Microphone(device_index=selected_mic_index)
        else:
            microphone = sr.Microphone()
        
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
        
        with microphone as source:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
        
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
    
    except Exception as e:
        return f"Microphone error: {e}"

def say_time():
    """Speak the current time"""
    try:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    except Exception as e:
        speak("Sorry, I couldn't get the current time")
        print(f"Time error: {e}")

def say_date():
    """Speak the current date"""
    try:
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")
    except Exception as e:
        speak("Sorry, I couldn't get the current date")
        print(f"Date error: {e}")

def say_weather():
    """Speak weather information"""
    try:
        # This is a simple implementation - you might want to use a real weather API
        speak("Weather feature is currently unavailable. Please check your local weather service.")
    except Exception as e:
        speak("Sorry, I couldn't get the weather information")
        print(f"Weather error: {e}")

def get_weather_info(city="London"):
    """Get weather information for a city (placeholder)"""
    # You would implement actual weather API call here
    # For now, return a placeholder
    return {
        "city": city,
        "temperature": "20°C",
        "condition": "Partly cloudy",
        "description": f"The weather in {city} is partly cloudy with a temperature of 20 degrees Celsius"
    }

def select_microphone_gui():
    """GUI for selecting microphone"""
    global selected_mic_index
    
    root = tk.Toplevel()
    root.title("Select Microphone")
    root.geometry("400x300")
    
    tk.Label(root, text="Available Microphones:", font=("Arial", 12)).pack(pady=10)
    
    mic_names = list_microphones()
    selected_mic = tk.StringVar(value=mic_names[0] if mic_names else "")
    
    listbox = tk.Listbox(root, font=("Arial", 10))
    listbox.pack(fill="both", expand=True, padx=20, pady=10)
    
    for i, mic in enumerate(mic_names):
        listbox.insert(tk.END, f"{i}: {mic}")
    
    def on_select():
        global selected_mic_index
        selection = listbox.curselection()
        if selection:
            selected_mic_index = selection[0]
            messagebox.showinfo("Success", f"Selected microphone: {mic_names[selected_mic_index]}")
            root.destroy()
    
    def on_test():
        selection = listbox.curselection()
        if selection:
            temp_index = selected_mic_index
            selected_mic_index = selection[0]
            speak("Testing microphone. Please say something.")
            result = listen_for_speech(timeout=3)
            messagebox.showinfo("Test Result", f"Recognized: {result}")
            selected_mic_index = temp_index
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Select", command=on_select, font=("Arial", 10)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Test", command=on_test, font=("Arial", 10)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Cancel", command=root.destroy, font=("Arial", 10)).pack(side="left", padx=5)

def process_voice_command(command_text):
    """Process voice commands"""
    command = command_text.lower().strip()
    
    if "time" in command:
        say_time()
    elif "date" in command:
        say_date()
    elif "weather" in command:
        say_weather()
    elif "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")
    elif "help" in command:
        speak("You can ask me for the time, date, weather, or say hello. What would you like to know?")
    else:
        speak(f"You said: {command_text}. I'm not sure how to help with that yet.")

# Initialize TTS when module is imported
init_tts()