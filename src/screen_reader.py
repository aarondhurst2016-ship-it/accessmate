
# --- Improved, cross-platform, unified screen reader ---
import sys

# --- Optimized for low-end devices ---
import pyttsx3
import speech_recognition as sr
import pyperclip
from PIL import ImageGrab, Image
import pytesseract

if sys.platform.startswith('win'):
    import pywinauto
    from pywinauto import Desktop

from weather import get_weather
from notes import create_note

engine = pyttsx3.init()

def speak(text, max_length=200):
    """
    Speak text, truncated for low-power devices. Avoid long TTS to save CPU/battery.
    """
    try:
        if len(text) > max_length:
            text = text[:max_length] + '...'
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

    # Removed OCR code from speak function as 'region' is not defined here.

def read_selected_text():
    """Read selected text from clipboard."""
    try:
        text = pyperclip.paste()
        if text.strip():
            speak(text)
            return text
        else:
            speak("Clipboard is empty or no text selected.")
            return None
    except Exception as e:
        speak(f"Error reading selected text: {e}")
        return None

def read_window_title():
    """Read the title of the foreground window (Windows only)."""
    if sys.platform.startswith('win'):
        try:
            window = Desktop(backend="uia").get_active()
            title = window.window_text()
            if title:
                speak(f"Window title: {title}")
                return title
            else:
                speak("No window title found.")
                return None
        except Exception as e:
            speak(f"Error reading window title: {e}")
            return None
    else:
        speak("Window title reading is only supported on Windows.")
        return None

def read_all_windows():
    """Read all visible text from all top-level windows (Windows, API) or OCR (other OS)."""
    if sys.platform.startswith('win'):
        try:
            texts = []
            for win in Desktop(backend="uia").windows():
                try:
                    win_texts = []
                    for ctrl in win.descendants():
                        t = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
                        if t and isinstance(t, str) and t.strip():
                            win_texts.append(t.strip())
                    if win_texts:
                        texts.append(f"Window: {win.window_text()}\n" + '\n'.join(win_texts))
                except Exception:
                    continue
            full_text = '\n\n'.join(texts)
            if full_text.strip():
                speak(full_text)
                return full_text
            else:
                speak("No readable text found in any window.")
                return None
        except Exception as e:
            speak(f"Error reading all windows: {e}")
            return None
    else:
        # Fallback: OCR entire screen
        text = ocr_screen_region()
        if text:
            speak(text)
            return text
        else:
            speak("No readable text found on screen.")
            return None

def read_foreground_window():
    """Read all visible text from the foreground window, with OCR fallback (cross-platform)."""
    if sys.platform.startswith('win'):
        try:
            window = Desktop(backend="uia").get_active()
            texts = []
            for ctrl in window.descendants():
                try:
                    t = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
                    if t and isinstance(t, str) and t.strip():
                        texts.append(t.strip())
                except Exception:
                    continue
            display_text = '\n'.join(texts).strip()
            if not display_text:
                # OCR fallback: grab window region
                rect = window.rectangle()
                display_text = ocr_screen_region((rect.left, rect.top, rect.right, rect.bottom))
            if display_text:
                speak(display_text)
                return display_text
            else:
                speak("No readable text found in foreground window.")
                return None
        except Exception as e:
            speak(f"Error reading foreground window: {e}")
            return None
    else:
        # Fallback: OCR entire screen
        text = ocr_screen_region()
        if text:
            speak(text)
            return text
        else:
            speak("No readable text found on screen.")
            return None

def read_screen():
    """Read text under mouse or OCR region (cross-platform)."""
    if sys.platform.startswith('win'):
        try:
            mouse_pos = pywinauto.mouse.get_cursor_pos()
            window = Desktop(backend="uia").from_point(*mouse_pos)
            ctrl = window.child_window(top_level_only=False, visible_only=True).from_point(*mouse_pos)
            text = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
            if text:
                speak(text)
                return text
            else:
                # OCR fallback: grab small region around mouse
                x, y = mouse_pos
                region = (x-100, y-30, x+100, y+30)
                ocr_text = ocr_screen_region(region)
                if ocr_text:
                    speak(ocr_text)
                    return ocr_text
                else:
                    speak("No readable text found under mouse.")
                    return None
        except Exception as e:
            speak(f"Error reading screen: {e}")
            return None
    else:
        # Fallback: OCR small region around center of screen (if pyautogui available)
        try:
            try:
                import pyautogui
                x, y = pyautogui.size()
                cx, cy = x//2, y//2
            except ImportError:
                # If pyautogui is not available, use default center
                cx, cy = 960, 540  # 1920x1080 default
            region = (cx-100, cy-30, cx+100, cy+30)
            ocr_text = ocr_screen_region(region)
            if ocr_text:
                speak(ocr_text)
                return ocr_text
            else:
                speak("No readable text found under mouse.")
                return None
        except Exception as e:
            speak(f"Error reading screen: {e}")
            return None

def save_spoken_text(text, filename="spoken_text.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        speak("Text saved to file.")
        return True
    except Exception as e:
        speak(f"Error saving text: {e}")
        return False

def handle_voice_command(command):
    command = command.lower()
    if "read screen" in command:
        speak("Reading screen now.")
        read_screen()
    elif "read window" in command or "read foreground" in command:
        speak("Reading foreground window now.")
        read_foreground_window()
    elif "read all windows" in command:
        speak("Reading all windows now.")
        read_all_windows()
    elif "read selected" in command or "read clipboard" in command:
        speak("Reading selected text.")
        read_selected_text()
    elif "read title" in command or "window title" in command:
        speak("Reading window title.")
        read_window_title()
    elif "save spoken" in command or "save text" in command:
        speak("Saving spoken text.")
        text = pyperclip.paste()
        if text.strip():
            save_spoken_text(text)
        else:
            speak("No text to save.")
    # Typing, pressing enter, closing window, clicking button, weather, note, etc. are not handled in this refactored version.

def listen_for_commands():
    recognizer = sr.Recognizer()
    try:
        print("Available microphones:")
        for idx, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {idx}: {name}")
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone error: {e}")
        speak(f"Microphone error: {e}")
        return

    speak("Say a command, like 'read screen', 'weather', or 'note'.")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        handle_voice_command(command)
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase.")
        speak("Listening timed out. Please try again.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
        speak("Could not understand audio. Please speak clearly.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak(f"Speech recognition service error: {e}")
    except Exception as e:
        print(f"General error: {e}")
        speak(f"Could not process command: {e}")

def test_speech_output(text="This is a test of the speech engine."):
    try:
        engine.say(text)
        engine.runAndWait()
        print("Speech output should have played.")
    except Exception as e:
        print(f"Speech engine error: {e}")

if __name__ == "__main__":
    print("Testing speech output...")
    test_speech_output()
    listen_for_commands()

    # --- Improved, cross-platform, unified screen reader ---
    import sys
    import time
    import pyttsx3
    import speech_recognition as sr
    import pyperclip
    from PIL import ImageGrab
    import pytesseract
    
    if sys.platform.startswith('win'):
        import pywinauto
        from pywinauto import Desktop
    
    from weather import get_weather
    from notes import create_note
    
    engine = pyttsx3.init()
    
    def speak(text):
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    
    def ocr_screen_region(region=None):
        try:
            img = ImageGrab.grab(bbox=region) if region else ImageGrab.grab()
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            return f"[OCR error: {e}]"
    
    def read_selected_text():
        """Read selected text from clipboard."""
        try:
            text = pyperclip.paste()
            if text.strip():
                speak(text)
                return text
            else:
                speak("Clipboard is empty or no text selected.")
                return None
        except Exception as e:
            speak(f"Error reading selected text: {e}")
            return None
    
    def read_window_title():
        """Read the title of the foreground window (Windows only)."""
        if sys.platform.startswith('win'):
            try:
                window = Desktop(backend="uia").get_active()
                title = window.window_text()
                if title:
                    speak(f"Window title: {title}")
                    return title
                else:
                    speak("No window title found.")
                    return None
            except Exception as e:
                speak(f"Error reading window title: {e}")
                return None
        else:
            speak("Window title reading is only supported on Windows.")
            return None
    
    def read_all_windows():
        """Read all visible text from all top-level windows (Windows, API) or OCR (other OS)."""
        if sys.platform.startswith('win'):
            try:
                from pywinauto import Desktop
                texts = []
                for win in Desktop(backend="uia").windows():
                    try:
                        win_texts = []
                        for ctrl in win.descendants():
                            t = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
                            if t and isinstance(t, str) and t.strip():
                                win_texts.append(t.strip())
                        if win_texts:
                            texts.append(f"Window: {win.window_text()}\n" + '\n'.join(win_texts))
                    except Exception:
                        continue
                full_text = '\n\n'.join(texts)
                if full_text.strip():
                    speak(full_text)
                    return full_text
                else:
                    speak("No readable text found in any window.")
                    return None
            except Exception as e:
                speak(f"Error reading all windows: {e}")
                return None
        else:
            # Fallback: OCR entire screen
            text = ocr_screen_region()
            if text:
                speak(text)
                return text
            else:
                speak("No readable text found on screen.")
                return None
    
    def read_foreground_window():
        """Read all visible text from the foreground window, with OCR fallback (cross-platform)."""
        if sys.platform.startswith('win'):
            try:
                window = Desktop(backend="uia").get_active()
                texts = []
                for ctrl in window.descendants():
                    try:
                        t = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
                        if t and isinstance(t, str) and t.strip():
                            texts.append(t.strip())
                    except Exception:
                        continue
                display_text = '\n'.join(texts).strip()
                if not display_text:
                    # OCR fallback: grab window region
                    rect = window.rectangle()
                    display_text = ocr_screen_region((rect.left, rect.top, rect.right, rect.bottom))
                if display_text:
                    speak(display_text)
                    return display_text
                else:
                    speak("No readable text found in foreground window.")
                    return None
            except Exception as e:
                speak(f"Error reading foreground window: {e}")
                return None
        else:
            # Fallback: OCR entire screen
            text = ocr_screen_region()
            if text:
                speak(text)
                return text
            else:
                speak("No readable text found on screen.")
                return None
    
    def read_screen():
        """Read text under mouse or OCR region (cross-platform)."""
        if sys.platform.startswith('win'):
            try:
                mouse_pos = pywinauto.mouse.get_cursor_pos()
                window = Desktop(backend="uia").from_point(*mouse_pos)
                ctrl = window.child_window(top_level_only=False, visible_only=True).from_point(*mouse_pos)
                text = ctrl.window_text() or ctrl.get_value() or ctrl.get_properties().get('name', '')
                if text:
                    speak(text)
                    return text
                else:
                    # OCR fallback: grab small region around mouse
                    x, y = mouse_pos
                    region = (x-100, y-30, x+100, y+30)
                    ocr_text = ocr_screen_region(region)
                    if ocr_text:
                        speak(ocr_text)
                        return ocr_text
                    else:
                        speak("No readable text found under mouse.")
                        return None
            except Exception as e:
                speak(f"Error reading screen: {e}")
                return None
        else:
            # Fallback: OCR small region around center of screen (if pyautogui available)
            try:
                try:
                    import pyautogui
                    x, y = pyautogui.size()
                    cx, cy = x//2, y//2
                except ImportError:
                    # If pyautogui is not available, use default center
                    cx, cy = 960, 540  # 1920x1080 default
                region = (cx-100, cy-30, cx+100, cy+30)
                ocr_text = ocr_screen_region(region)
                if ocr_text:
                    speak(ocr_text)
                    return ocr_text
                else:
                    speak("No readable text found under mouse.")
                    return None
            except Exception as e:
                speak(f"Error reading screen: {e}")
                return None
    
    def save_spoken_text(text, filename="spoken_text.txt"):
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            speak("Text saved to file.")
            return True
        except Exception as e:
            speak(f"Error saving text: {e}")
            return False
    
    def handle_voice_command(command):
        command = command.lower()
        if "read screen" in command:
            speak("Reading screen now.")
            read_screen()
        elif "read window" in command or "read foreground" in command:
            speak("Reading foreground window now.")
            read_foreground_window()
        elif "read all windows" in command:
            speak("Reading all windows now.")
            read_all_windows()
        elif "read selected" in command or "read clipboard" in command:
            speak("Reading selected text.")
            read_selected_text()
        elif "read title" in command or "window title" in command:
            speak("Reading window title.")
            read_window_title()
        elif "save spoken" in command or "save text" in command:
            speak("Saving spoken text.")
            text = pyperclip.paste()
            if text.strip():
                save_spoken_text(text)
            else:
                speak("No text to save.")
        # Typing, pressing enter, closing window, clicking button, weather, note, etc. are not handled in this refactored version.
    
    def listen_for_commands():
        recognizer = sr.Recognizer()
        try:
            print("Available microphones:")
            for idx, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"  {idx}: {name}")
            mic = sr.Microphone()
        except Exception as e:
            print(f"Microphone error: {e}")
            speak(f"Microphone error: {e}")
            return
    
        speak("Say a command, like 'read screen', 'weather', or 'note'.")
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for command...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            # Call the command handler (define this function above)
            handle_voice_command(command)
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase.")
            speak("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("Could not understand audio. Please speak clearly.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak(f"Speech recognition service error: {e}")
        except Exception as e:
            print(f"General error: {e}")
            speak(f"Could not process command: {e}")
    
    def test_speech_output(text="This is a test of the speech engine."):
        try:
            engine.say(text)
            engine.runAndWait()
            print("Speech output should have played.")
        except Exception as e:
            print(f"Speech engine error: {e}")


def listen_for_commands():
    recognizer = sr.Recognizer()
    # Microphone diagnostics
    try:
        print("Available microphones:")
        for idx, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {idx}: {name}")
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone error: {e}")
        engine.say(f"Microphone error: {e}")
        engine.runAndWait()
        return

    engine.say("Say a command, like 'read screen', 'weather', or 'note'.")
    engine.runAndWait()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        handle_voice_command(command)
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase.")
        engine.say("Listening timed out. Please try again.")
        engine.runAndWait()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        engine.say("Could not understand audio. Please speak clearly.")
        engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine.say(f"Speech recognition service error: {e}")
        engine.runAndWait()
    except Exception as e:
        print(f"General error: {e}")
        engine.say(f"Could not process command: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    print("Testing speech output...")
    test_speech_output()
    listen_for_commands()
