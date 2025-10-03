"""
Universal screen reader for Windows (API + OCR fallback)
- Tries to read text from the active window using pywinauto (UI Automation)
- Falls back to OCR (pytesseract) on a screenshot if API fails or returns no text
- Designed for integration with Talkback Assistant
"""
import sys
import platform

from PIL import ImageGrab
import pytesseract

# Only import pywinauto on Windows
if platform.system() == "Windows":
    from pywinauto import Desktop
else:
    Desktop = None

def read_active_window_text():
    """Try to read text from the active window using accessibility API, fallback to OCR."""
    text = ""
    if Desktop:
        try:
            win = Desktop(backend="uia").get_active()
            # Try to get all text controls
            texts = []
            for ctrl in win.descendants():
                try:
                    val = ctrl.window_text()
                    if val:
                        texts.append(val)
                except Exception:
                    continue
            text = "\n".join(texts)
        except Exception:
            pass
    if not text:
        # Fallback: OCR on screenshot of active window
        try:
            if Desktop:
                win = Desktop(backend="uia").get_active()
                rect = win.rectangle()
                img = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
            else:
                img = ImageGrab.grab()
            text = pytesseract.image_to_string(img)
        except Exception as e:
            text = f"[Error capturing screen: {e}]"
    return text

if __name__ == "__main__":
    print(read_active_window_text())
