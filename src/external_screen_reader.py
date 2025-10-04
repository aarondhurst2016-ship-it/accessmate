"""
External Screen Reader Module for AccessMate
Provides system-wide screen reading capabilities outside the app
"""

import sys
import os
import time
import threading
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class ScreenReaderConfig:
    """Configuration for external screen reader"""
    hotkey_read_window: str = "ctrl+shift+r"
    hotkey_read_cursor: str = "ctrl+shift+c"
    hotkey_read_selection: str = "ctrl+shift+s"
    hotkey_toggle_continuous: str = "ctrl+shift+t"
    voice_rate: int = 200
    voice_volume: float = 0.8
    auto_announce_focus: bool = True

class ExternalScreenReader:
    """External screen reader for reading content from any application"""
    
    def __init__(self, config: ScreenReaderConfig = None):
        self.config = config or ScreenReaderConfig()
        self.is_running = False
        self.continuous_mode = False
        self.last_focused_window = None
        self.current_text = ""
        
        # Import platform-specific modules
        self._init_platform_modules()
        self._setup_hotkeys()
    
    def _init_platform_modules(self):
        """Initialize platform-specific accessibility modules"""
        try:
            if sys.platform.startswith('win'):
                import pyautogui
                import pygetwindow as gw
                import pyperclip
                self.pyautogui = pyautogui
                self.gw = gw
                self.pyperclip = pyperclip
                
                # Try to import Windows-specific accessibility
                try:
                    import pywinauto
                    self.pywinauto = pywinauto
                    self.windows_api_available = True
                except ImportError:
                    self.windows_api_available = False
                    print("pywinauto not available - some features limited")
                    
        except ImportError as e:
            print(f"Screen reader dependencies not available: {e}")
            self.dependencies_available = False
        else:
            self.dependencies_available = True
    
    def _setup_hotkeys(self):
        """Setup global hotkeys for screen reading"""
        try:
            import keyboard
            self.keyboard = keyboard
            
            # Register global hotkeys
            keyboard.add_hotkey(self.config.hotkey_read_window, self.read_active_window)
            keyboard.add_hotkey(self.config.hotkey_read_cursor, self.read_at_cursor)
            keyboard.add_hotkey(self.config.hotkey_read_selection, self.read_selection)
            keyboard.add_hotkey(self.config.hotkey_toggle_continuous, self.toggle_continuous_mode)
            
            print("External screen reader hotkeys registered:")
            print(f"  {self.config.hotkey_read_window} - Read active window")
            print(f"  {self.config.hotkey_read_cursor} - Read at cursor")
            print(f"  {self.config.hotkey_read_selection} - Read selection")
            print(f"  {self.config.hotkey_toggle_continuous} - Toggle continuous mode")
            
        except ImportError:
            print("keyboard module not available - hotkeys disabled")
            self.keyboard = None
    
    def start(self):
        """Start the external screen reader"""
        if not self.dependencies_available:
            print("Cannot start external screen reader - dependencies missing")
            return False
            
        self.is_running = True
        print("External screen reader started")
        
        # Start background monitoring thread if continuous mode
        if self.config.auto_announce_focus:
            self._start_focus_monitoring()
        
        return True
    
    def stop(self):
        """Stop the external screen reader"""
        self.is_running = False
        self.continuous_mode = False
        print("External screen reader stopped")
    
    def _start_focus_monitoring(self):
        """Start monitoring window focus changes"""
        def monitor_focus():
            while self.is_running:
                try:
                    if self.continuous_mode:
                        current_window = self._get_active_window()
                        if current_window and current_window != self.last_focused_window:
                            self.last_focused_window = current_window
                            self._announce_window_change(current_window)
                    time.sleep(0.5)  # Check every 500ms
                except Exception as e:
                    print(f"Focus monitoring error: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=monitor_focus, daemon=True)
        thread.start()
    
    def read_active_window(self):
        """Read the content of the currently active window"""
        if not self.is_running:
            return
            
        try:
            window_text = self._get_window_text()
            if window_text:
                self._speak(f"Reading active window: {window_text}")
            else:
                self._speak("No readable text found in active window")
        except Exception as e:
            print(f"Error reading active window: {e}")
            self._speak("Error reading active window")
    
    def read_at_cursor(self):
        """Read text at the current cursor position"""
        if not self.is_running:
            return
            
        try:
            # Try multiple methods to get text at cursor
            text = self._get_text_at_cursor()
            if text:
                self._speak(f"At cursor: {text}")
            else:
                self._speak("No text found at cursor position")
        except Exception as e:
            print(f"Error reading at cursor: {e}")
            self._speak("Error reading at cursor position")
    
    def read_selection(self):
        """Read currently selected text"""
        if not self.is_running:
            return
            
        try:
            # Save current clipboard
            original_clipboard = self._get_clipboard()
            
            # Copy selection to clipboard
            self.pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)  # Wait for copy operation
            
            # Get selected text
            selected_text = self._get_clipboard()
            
            if selected_text and selected_text != original_clipboard:
                self._speak(f"Selected text: {selected_text}")
            else:
                self._speak("No text selected")
                
            # Restore original clipboard if it changed
            if original_clipboard:
                self._set_clipboard(original_clipboard)
                
        except Exception as e:
            print(f"Error reading selection: {e}")
            self._speak("Error reading selection")
    
    def toggle_continuous_mode(self):
        """Toggle continuous reading mode on/off"""
        self.continuous_mode = not self.continuous_mode
        status = "enabled" if self.continuous_mode else "disabled"
        self._speak(f"Continuous reading mode {status}")
        print(f"Continuous mode: {status}")
    
    def _get_active_window(self):
        """Get the currently active window"""
        try:
            if hasattr(self, 'gw'):
                return self.gw.getActiveWindow()
        except:
            pass
        return None
    
    def _get_window_text(self):
        """Get readable text from the active window"""
        try:
            # Method 1: Try using pywinauto for Windows accessibility
            if self.windows_api_available and sys.platform.startswith('win'):
                text = self._get_text_via_accessibility()
                if text:
                    return text
            
            # Method 2: Try getting window title and basic info
            window = self._get_active_window()
            if window:
                title = getattr(window, 'title', 'Untitled')
                return f"Window: {title}"
                
        except Exception as e:
            print(f"Error getting window text: {e}")
        
        return None
    
    def _get_text_via_accessibility(self):
        """Get text using Windows accessibility APIs"""
        try:
            from pywinauto import Application
            
            # Get the active window
            active_window = self._get_active_window()
            if not active_window:
                return None
            
            # Try to connect to the application
            app = Application().connect(handle=active_window._hWnd)
            window = app.window(handle=active_window._hWnd)
            
            # Get window text content
            texts = []
            
            # Try to get all text controls
            for control in window.descendants():
                try:
                    if hasattr(control, 'window_text'):
                        text = control.window_text()
                        if text and text.strip():
                            texts.append(text.strip())
                except:
                    continue
            
            if texts:
                return " ".join(texts[:10])  # Limit to first 10 text elements
                
        except Exception as e:
            print(f"Accessibility API error: {e}")
        
        return None
    
    def _get_text_at_cursor(self):
        """Get text at the current cursor position"""
        try:
            # Method 1: Try to select word at cursor and read it
            current_pos = self.pyautogui.position()
            
            # Double-click to select word at cursor
            self.pyautogui.doubleClick()
            time.sleep(0.1)
            
            # Copy selected text
            original_clipboard = self._get_clipboard()
            self.pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            selected_text = self._get_clipboard()
            
            # Click somewhere else to deselect
            self.pyautogui.click(current_pos)
            
            # Restore clipboard
            if original_clipboard:
                self._set_clipboard(original_clipboard)
            
            return selected_text if selected_text != original_clipboard else None
            
        except Exception as e:
            print(f"Error getting text at cursor: {e}")
        
        return None
    
    def _announce_window_change(self, window):
        """Announce when window focus changes"""
        try:
            title = getattr(window, 'title', 'Unknown window')
            self._speak(f"Switched to {title}")
        except Exception as e:
            print(f"Error announcing window change: {e}")
    
    def _get_clipboard(self):
        """Get clipboard content"""
        try:
            return self.pyperclip.paste()
        except:
            return ""
    
    def _set_clipboard(self, text):
        """Set clipboard content"""
        try:
            self.pyperclip.copy(text)
        except:
            pass
    
    def _speak(self, text):
        """Speak text using the speech engine"""
        try:
            # Try to use the main app's speech module
            sys.path.append(os.path.dirname(__file__))
            import speech
            speech.speak(text)
        except:
            # Fallback to print
            print(f"Screen Reader: {text}")

# Global screen reader instance
_screen_reader = None

def start_external_screen_reader(config: ScreenReaderConfig = None):
    """Start the external screen reader"""
    global _screen_reader
    
    if _screen_reader and _screen_reader.is_running:
        print("External screen reader already running")
        return _screen_reader
    
    _screen_reader = ExternalScreenReader(config)
    success = _screen_reader.start()
    
    if success:
        print("External screen reader started successfully")
        print("Use the following hotkeys to read content from any application:")
        print("  Ctrl+Shift+R - Read active window")
        print("  Ctrl+Shift+C - Read at cursor position")
        print("  Ctrl+Shift+S - Read selected text")
        print("  Ctrl+Shift+T - Toggle continuous mode")
    
    return _screen_reader

def stop_external_screen_reader():
    """Stop the external screen reader"""
    global _screen_reader
    
    if _screen_reader:
        _screen_reader.stop()
        _screen_reader = None
        print("External screen reader stopped")

def get_screen_reader():
    """Get the current screen reader instance"""
    return _screen_reader

if __name__ == "__main__":
    # Test the external screen reader
    print("Starting external screen reader test...")
    reader = start_external_screen_reader()
    
    if reader:
        print("Screen reader started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_external_screen_reader()
            print("Screen reader stopped.")