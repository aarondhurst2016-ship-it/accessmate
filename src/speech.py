from googletrans import Translator

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    try:
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception:
        return text
# Speech module for Talkback Assistant

from gtts import gTTS
import pygame
import speech_recognition as sr

# Microphone selection setting

# Microphone selection setting
selected_mic_index = None  # Set to None for default, or set to an integer for a specific mic

def select_microphone_gui():
    import tkinter as tk
    from tkinter import simpledialog
    mics = list_microphones()
    root = tk.Tk()
    root.withdraw()
    mic_list = "\n".join([f"{i}: {name}" for i, name in enumerate(mics)])
    msg = f"Available microphones:\n{mic_list}\n\nEnter the index of the microphone to use:"
    idx = simpledialog.askinteger("Select Microphone", msg)
    global selected_mic_index
    if idx is not None and 0 <= idx < len(mics):
        selected_mic_index = idx
        print(f"Microphone selected: {mics[idx]} (index {idx})")
    else:
        selected_mic_index = None
        print("Default microphone will be used.")

def list_microphones():
    """Returns a list of available microphone names."""
    return sr.Microphone.list_microphone_names()

def speak(text, lang='en'):
    import tempfile, os
    from gtts.lang import tts_langs
    supported_langs = tts_langs()
    if lang not in supported_langs:
        err_msg = f"[ERROR] Language code '{lang}' is not supported by gTTS. Supported codes: {', '.join(sorted(supported_langs.keys()))}"
        print(err_msg)
        # Optionally, speak the error in English if possible
        if lang != 'en':
            try:
                tts = gTTS(text=err_msg, lang='en')
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
                    temp_filename = tf.name
                tts.save(temp_filename)
                pygame.mixer.init()
                pygame.mixer.music.load(temp_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                os.remove(temp_filename)
            except Exception:
                pass
        return
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
        temp_filename = tf.name
    tts.save(temp_filename)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove(temp_filename)


def say_time(lang='en'):
    import datetime
    now = datetime.datetime.now()
    time_str = now.strftime('%I:%M %p')
    speak(f"The time is {time_str}", lang=lang)

def say_date(lang='en'):
    import datetime
    now = datetime.datetime.now()
    date_str = now.strftime('%A, %B %d, %Y')
    speak(f"Today is {date_str}", lang=lang)

def say_weather(city=None, lang='en'):
    from weather import get_weather
    try:
        if city is None:
            from location import get_location
            city = get_location()
            if not city or city == "Unknown":
                city = "London"
        weather_str = get_weather(city)
        speak(f"Weather: {weather_str}", lang=lang)
    except Exception as e:
        speak(f"Weather error: {e}", lang=lang)

def listen_and_translate(src_lang, dest_lang):
    text = listen(src_lang)
    if text:
        translated = translate_text(text, src_lang, dest_lang)
        print(f"Translated: {translated}")
        return translated
    return None

def listen(lang='en', timeout=2, phrase_time_limit=3):
    global selected_mic_index
    recognizer = sr.Recognizer()
    mic_index = selected_mic_index
    print(f"[DEBUG] listen() using mic index: {mic_index}")
    if mic_index is None:
        source = sr.Microphone()
    else:
        source = sr.Microphone(device_index=mic_index)
    with source as src:
        print(f"Listening on mic index {mic_index if mic_index is not None else 'default'}...")
        audio = recognizer.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = recognizer.recognize_google(audio, language=lang)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
