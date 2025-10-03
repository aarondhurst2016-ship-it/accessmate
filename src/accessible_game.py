# Voice-to-keyboard controller for any running game
import threading
try:
    import speech_recognition as sr
    import pyttsx3
    import pyautogui
except ImportError:
    sr = None
    pyttsx3 = None
    pyautogui = None

def voice_game_controller(command_map=None, tts_func=None):
    """
    Listens for voice commands and sends mapped keyboard keys to the OS.
    command_map: dict mapping spoken words to keyboard keys, e.g. {'jump': 'space', 'left': 'left', ...}
    tts_func: function to speak feedback.
    """
    if sr is None or pyautogui is None:
        print("speech_recognition and pyautogui are required for voice game control.")
        return
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    if tts_func is None:
        def tts_func(text):
            if pyttsx3:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            else:
                print(f"[TTS] {text}")
    if command_map is None:
        command_map = {'jump': 'space', 'left': 'left', 'right': 'right', 'up': 'up', 'down': 'down', 'shoot': 'ctrl'}
    tts_func("Voice game controller started. Say a command like 'jump', 'left', or 'shoot'. Say 'exit' to stop.")
    running = True
    def listen_loop():
        nonlocal running
        while running:
            with mic as source:
                tts_func("Listening for game command...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio).strip().lower()
                except Exception:
                    continue
            if text == 'exit':
                tts_func("Voice game controller stopped.")
                running = False
                break
            key = command_map.get(text)
            if key:
                pyautogui.press(key)
                tts_func(f"Sent key: {key}")
            else:
                tts_func(f"Unknown command: {text}")
    thread = threading.Thread(target=listen_loop, daemon=True)
    thread.start()
"""
Accessible Audio Game Module
A simple audio-based game for blind/low-vision users, with voice and haptic feedback support.
"""
import random
import time
import threading
try:
    import pygame
except ImportError:
    pygame = None

class AccessibleAudioGame:
    def __init__(self, tts_func=None, stt_func=None, haptic_func=None):
        self.tts = tts_func or self.default_tts
        self.stt = stt_func or self.default_stt
        self.haptic = haptic_func or self.default_haptic
        self.running = False
        self.score = 0
        if pygame:
            pygame.mixer.init()

    def default_tts(self, text):
        print(f"[TTS] {text}")

    def default_stt(self, prompt):
        try:
            import speech_recognition as sr
        except ImportError:
            return input(f"[Voice Input] {prompt}")
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        self.tts(prompt)
        with mic as source:
            audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except Exception:
            self.tts("Sorry, I didn't catch that. Please try again.")
            return ""

    def default_haptic(self, pattern):
        print(f"[Haptic] {pattern}")

    def play_sound(self, sound_file):
        if pygame:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        else:
            print(f"[Sound] {sound_file}")

    def start(self):
        self.tts("Welcome to the accessible audio game! Listen for the sound and say 'hit' as fast as you can. Use your voice to play.")
        self.running = True
        self.score = 0
        for round_num in range(3):
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)
            self.tts("Get ready!")
            self.haptic("buzz")
            self.play_sound("beep.wav")  # Replace with actual sound file
            start_time = time.time()
            response = self.stt("Say 'hit' now!")
            reaction = time.time() - start_time
            if response.strip().lower() == "hit" and reaction < 2.0:
                self.tts(f"Good job! Reaction time: {reaction:.2f} seconds.")
                self.haptic("success")
                self.score += 1
            else:
                self.tts("Too slow or wrong word. Try again!")
                self.haptic("fail")
        self.tts(f"Game over! Your score: {self.score}/3")
        self.running = False

# Example usage:
if __name__ == "__main__":
    game = AccessibleAudioGame()
    game.start()
