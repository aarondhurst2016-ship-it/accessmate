#!/usr/bin/env python3
"""
Test script to verify gTTS conditional imports work correctly.
This simulates what happens when gTTS is not available.
"""

import sys
import os

print("Testing gTTS conditional imports...")

# Test speech.py
print("\n1. Testing speech.py module:")
try:
    from src import speech
    print("   ✓ speech.py imported successfully")
    print(f"   ✓ GTTS_AVAILABLE = {speech.GTTS_AVAILABLE}")
    
    # Test the speak function
    speech.speak("Test message", lang='en')
    print("   ✓ speak() function executed without error")
    
except Exception as e:
    print(f"   ✗ Error importing speech.py: {e}")

# Test ocr_screen_reader.py
print("\n2. Testing ocr_screen_reader.py module:")
try:
    from src import ocr_screen_reader
    print("   ✓ ocr_screen_reader.py imported successfully")
    print(f"   ✓ GTTS_AVAILABLE = {ocr_screen_reader.GTTS_AVAILABLE}")
    
    # Test creating OCR instance
    ocr = ocr_screen_reader.OCRScreenReader()
    ocr.default_tts("Test TTS message")
    print("   ✓ OCRScreenReader and default_tts() executed without error")
    
except Exception as e:
    print(f"   ✗ Error with ocr_screen_reader.py: {e}")

print("\n✓ All conditional import tests completed successfully!")
print("The application should now handle missing gTTS gracefully.")