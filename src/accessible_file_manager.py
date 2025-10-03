
"""
accessible_file_manager.py - Cross-platform accessible file manager backend
Features: list files/folders, open/read, rename, delete, read aloud
"""
import os
import sys

def list_dir(path=None):
    """List files and folders in the given directory."""
    if not path:
        path = os.path.expanduser("~")
    try:
        items = os.listdir(path)
        result = []
        for item in items:
            full = os.path.join(path, item)
            result.append({
                "name": item,
                "is_dir": os.path.isdir(full),
                "path": full
            })
        return result
    except Exception as e:
        return []

def read_file(file_path, max_bytes=100000):
    """Read file content (text, up to max_bytes)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_bytes)
    except Exception:
        return None

def delete_file(file_path):
    try:
        os.remove(file_path)
        return True
    except Exception:
        return False

def rename_file(file_path, new_name):
    dir_ = os.path.dirname(file_path)
    new_path = os.path.join(dir_, new_name)
    try:
        os.rename(file_path, new_path)
        return new_path
    except Exception:
        return None

def read_file_aloud(file_path, platform="desktop"):
    """Read file aloud using TTS. Platform: 'desktop' (pyttsx3) or 'mobile' (gtts+pygame)."""
    text = read_file(file_path, max_bytes=5000)
    if not text:
        return False
    if platform == "desktop":
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception:
            return False
    else:
        try:
            from gtts import gTTS
            import pygame
            tts = gTTS(text)
            tts.save("temp_tts.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("temp_tts.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            os.remove("temp_tts.mp3")
            return True
        except Exception:
            return False
