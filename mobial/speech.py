from googletrans import Translator

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    try:
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text
    except Exception:
        return text
from plyer import tts
import speech_recognition as sr

def speak(text, lang='en'):
    try:
        tts.speak(text)
    except Exception as e:
        print(f"TTS error: {e}")

def listen(lang='en'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something:")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=lang)
        print(f"You said: {text}")
        return text
    except Exception:
        print("Sorry, I could not understand.")
        return None

def listen_and_translate(src_lang, dest_lang):
    text = listen(src_lang)
    if text:
        translated = translate_text(text, src_lang, dest_lang)
        print(f"Translated: {translated}")
        return translated
    return None
