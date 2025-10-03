# voice_notes.py
# Voice notes feature

import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import datetime

VOICE_NOTES_DIR = os.path.join(os.path.dirname(__file__), '../voice_notes')
os.makedirs(VOICE_NOTES_DIR, exist_ok=True)

def record_voice_note(duration=10, fs=16000):
    print("Recording voice note...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait(timeout=duration + 1)  # Automatically stop after duration
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(VOICE_NOTES_DIR, f'note_{timestamp}.wav')
    wav.write(filename, fs, audio)
    # Transcribe
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except Exception as e:
            text = "Could not transcribe: " + str(e)
    # Save transcription
    with open(filename.replace('.wav', '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Voice note saved: {filename}\nTranscription: {text}")
    return filename, text

def list_voice_notes():
    notes = []
    for fname in os.listdir(VOICE_NOTES_DIR):
        if fname.endswith('.wav'):
            txt_file = fname.replace('.wav', '.txt')
            txt_path = os.path.join(VOICE_NOTES_DIR, txt_file)
            text = None
            if os.path.exists(txt_path):
                with open(txt_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            notes.append({'audio': os.path.join(VOICE_NOTES_DIR, fname), 'text': text})
    return notes
