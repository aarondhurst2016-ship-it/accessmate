# Platform Compatibility Checker for Talkback Assistant
import sys
import platform

enable_accessibility = True   # global

def check_platform():
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    # Check Tkinter
    try:
        import tkinter
        print("Tkinter: OK")
    except ImportError:
        print("Tkinter: NOT FOUND")
    # Check gTTS
    try:
        import gtts
        print("gTTS: OK")
    except ImportError:
        print("gTTS: NOT FOUND")
    # Check pygame
    try:
        import pygame
        print("pygame: OK")
    except ImportError:
        print("pygame: NOT FOUND")
    # Check speech_recognition
    try:
        import speech_recognition
        print("speech_recognition: OK")
    except ImportError:
        print("speech_recognition: NOT FOUND")
    # Check Twilio
    try:
        import twilio
        print("Twilio: OK")
    except ImportError:
        print("Twilio: NOT FOUND")
    # Check requests
    try:
        import requests
        print("requests: OK")
    except ImportError:
        print("requests: NOT FOUND")
    # Check BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        print("BeautifulSoup: OK")
    except ImportError:
        print("BeautifulSoup: NOT FOUND")
    # Check FPDF
    try:
        import fpdf
        print("FPDF: OK")
    except ImportError:
        print("FPDF: NOT FOUND")

def launch_gui():
    print(enable_accessibility)  # works

if __name__ == "__main__":
    check_platform()
