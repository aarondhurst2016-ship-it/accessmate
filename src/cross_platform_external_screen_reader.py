"""
Cross-Platform External Screen Reader for AccessMate
Provides system-wide screen reading capabilities on Windows, macOS, and Linux
"""

import sys
import os
import time
import threading
import platform
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

class CrossPlatformExternalScreenReader:
    """Cross-platform external screen reader for reading content from any application"""
    
    def __init__(self, config: ScreenReaderConfig = None):
        self.config = config or ScreenReaderConfig()
        self.is_running = False
        self.continuous_mode = False
        self.last_focused_window = None
        self.current_text = ""
        self.platform = platform.system().lower()
        
        print(f"Initializing external screen reader for {self.platform}")
        
        # Initialize platform-specific modules
        self._init_platform_modules()
        self._setup_hotkeys()
    
    def _init_platform_modules(self):
        """Initialize platform-specific accessibility modules"""
        self.dependencies_available = False
        
        try:
            # Common modules for all platforms
            import pyautogui
            import pyperclip
            self.pyautogui = pyautogui
            self.pyperclip = pyperclip
            
            if self.platform == 'windows':
                self._init_windows_modules()
            elif self.platform == 'darwin':  # macOS
                self._init_macos_modules()
            elif self.platform == 'linux':
                self._init_linux_modules()
            else:
                print(f"Platform {self.platform} not fully supported")
                self.dependencies_available = False
                return
                
        except ImportError as e:
            print(f"Screen reader dependencies not available: {e}")
            self.dependencies_available = False
        else:
            self.dependencies_available = True
    
    def _init_windows_modules(self):
        """Initialize Windows-specific modules"""
        try:
            import pygetwindow as gw
            self.gw = gw
            
            # Try to import Windows-specific accessibility
            try:
                import pywinauto
                self.pywinauto = pywinauto
                self.windows_api_available = True
                print("Windows accessibility APIs loaded successfully")
            except ImportError:
                self.windows_api_available = False
                print("pywinauto not available - some Windows features limited")
                
        except ImportError as e:
            print(f"Windows modules not available: {e}")
            raise
    
    def _init_macos_modules(self):
        """Initialize macOS-specific modules"""
        try:
            # Try to import macOS-specific modules
            try:
                import AppKit  # type: ignore
                import Quartz  # type: ignore
                from AppKit import NSWorkspace, NSApp  # type: ignore
                from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID  # type: ignore
                
                self.AppKit = AppKit
                self.Quartz = Quartz
                self.NSWorkspace = NSWorkspace
                self.CGWindowListCopyWindowInfo = CGWindowListCopyWindowInfo
                self.macos_api_available = True
                print("macOS accessibility APIs loaded successfully")
                
            except ImportError:
                self.macos_api_available = False
                print("macOS APIs not available - some features limited")
                
        except Exception as e:
            print(f"macOS modules initialization failed: {e}")
            self.macos_api_available = False
    
    def _init_linux_modules(self):
        """Initialize Linux-specific modules"""
        try:
            # Try to import Linux-specific modules
            try:
                import subprocess
                import Xlib  # type: ignore
                from Xlib import display  # type: ignore
                from Xlib.X import AnyPropertyType  # type: ignore
                
                self.subprocess = subprocess
                self.Xlib = Xlib
                self.display = display
                self.linux_api_available = True
                print("Linux X11 APIs loaded successfully")
                
            except ImportError:
                try:
                    # Fallback to basic subprocess only
                    import subprocess
                    self.subprocess = subprocess
                    self.linux_api_available = False
                    print("X11 not available - using basic Linux support")
                except ImportError:
                    print("No Linux APIs available")
                    raise
                    
        except Exception as e:
            print(f"Linux modules initialization failed: {e}")
            self.linux_api_available = False
    
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
            
            print(f"External screen reader hotkeys registered for {self.platform}:")
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
            print(f"Cannot start external screen reader on {self.platform} - dependencies missing")
            return False
            
        self.is_running = True
        print(f"External screen reader started on {self.platform}")
        
        # Start background monitoring thread if continuous mode
        if self.config.auto_announce_focus:
            self._start_focus_monitoring()
        
        return True
    
    def stop(self):
        """Stop the external screen reader"""
        self.is_running = False
        self.continuous_mode = False
        print(f"External screen reader stopped on {self.platform}")
    
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
            if self.platform == 'darwin':
                self.pyautogui.hotkey('cmd', 'c')
            else:
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
        """Get the currently active window (platform-specific)"""
        try:
            if self.platform == 'windows':
                return self._get_windows_active_window()
            elif self.platform == 'darwin':
                return self._get_macos_active_window()
            elif self.platform == 'linux':
                return self._get_linux_active_window()
        except Exception as e:
            print(f"Error getting active window: {e}")
        return None
    
    def _get_windows_active_window(self):
        """Get active window on Windows"""
        try:
            if hasattr(self, 'gw'):
                return self.gw.getActiveWindow()
        except:
            pass
        return None
    
    def _get_macos_active_window(self):
        """Get active window on macOS"""
        try:
            if self.macos_api_available:
                workspace = self.NSWorkspace.sharedWorkspace()
                active_app = workspace.activeApplication()
                return active_app.get('NSApplicationName', 'Unknown')
        except Exception as e:
            print(f"macOS active window error: {e}")
        return None
    
    def _get_linux_active_window(self):
        """Get active window on Linux"""
        try:
            if hasattr(self, 'subprocess'):
                # Try using xdotool
                result = self.subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                           capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
                
                # Fallback to wmctrl
                result = self.subprocess.run(['wmctrl', '-v'], capture_output=True, text=True)
                if result.returncode == 0:
                    return "Linux Desktop"
        except Exception as e:
            print(f"Linux active window error: {e}")
        return None
    
    def _get_window_text(self):
        """Get readable text from the active window (platform-specific)"""
        try:
            if self.platform == 'windows':
                return self._get_windows_window_text()
            elif self.platform == 'darwin':
                return self._get_macos_window_text()
            elif self.platform == 'linux':
                return self._get_linux_window_text()
        except Exception as e:
            print(f"Error getting window text: {e}")
        return None
    
    def _get_windows_window_text(self):
        """Get window text on Windows"""
        try:
            # Method 1: Try using pywinauto for Windows accessibility
            if self.windows_api_available:
                text = self._get_text_via_windows_accessibility()
                if text:
                    return text
            
            # Method 2: Try getting window title and basic info
            window = self._get_active_window()
            if window:
                title = getattr(window, 'title', 'Untitled')
                return f"Window: {title}"
                
        except Exception as e:
            print(f"Windows window text error: {e}")
        return None
    
    def _get_macos_window_text(self):
        """Get window text on macOS"""
        try:
            if self.macos_api_available:
                # Get active application info
                workspace = self.NSWorkspace.sharedWorkspace()
                active_app = workspace.activeApplication()
                app_name = active_app.get('NSApplicationName', 'Unknown')
                return f"macOS Application: {app_name}"
        except Exception as e:
            print(f"macOS window text error: {e}")
        return None
    
    def _get_linux_window_text(self):
        """Get window text on Linux"""
        try:
            if hasattr(self, 'subprocess'):
                # Try getting window title with xdotool
                result = self.subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                           capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Linux Window: {result.stdout.strip()}"
        except Exception as e:
            print(f"Linux window text error: {e}")
        return None
    
    def _get_text_via_windows_accessibility(self):
        """Get text using Windows accessibility APIs"""
        try:
            if not self.windows_api_available:
                return None
                
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
            print(f"Windows accessibility API error: {e}")
        
        return None
    
    def _get_text_at_cursor(self):
        """Get text at the current cursor position (cross-platform)"""
        try:
            # Method 1: Try to select word at cursor and read it
            current_pos = self.pyautogui.position()
            
            # Double-click to select word at cursor
            self.pyautogui.doubleClick()
            time.sleep(0.1)
            
            # Copy selected text
            original_clipboard = self._get_clipboard()
            if self.platform == 'darwin':
                self.pyautogui.hotkey('cmd', 'c')
            else:
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
            if isinstance(window, str):
                title = window
            else:
                title = getattr(window, 'title', str(window))
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
            print(f"Screen Reader ({self.platform}): {text}")

# Global screen reader instance
_screen_reader = None

def start_cross_platform_external_screen_reader(config: ScreenReaderConfig = None):
    """Start the cross-platform external screen reader"""
    global _screen_reader
    
    if _screen_reader and _screen_reader.is_running:
        print("External screen reader already running")
        return _screen_reader
    
    _screen_reader = CrossPlatformExternalScreenReader(config)
    success = _screen_reader.start()
    
    if success:
        platform_name = _screen_reader.platform.title()
        print(f"External screen reader started successfully on {platform_name}")
        print("Use the following hotkeys to read content from any application:")
        print("  Ctrl+Shift+R - Read active window")
        print("  Ctrl+Shift+C - Read at cursor position")
        print("  Ctrl+Shift+S - Read selected text")
        print("  Ctrl+Shift+T - Toggle continuous mode")
    
    return _screen_reader

def stop_cross_platform_external_screen_reader():
    """Stop the cross-platform external screen reader"""
    global _screen_reader
    
    if _screen_reader:
        _screen_reader.stop()
        _screen_reader = None
        print("Cross-platform external screen reader stopped")

def get_cross_platform_screen_reader():
    """Get the current cross-platform screen reader instance"""
    return _screen_reader

# Backwards compatibility functions - use cross-platform versions
start_external_screen_reader = start_cross_platform_external_screen_reader
stop_external_screen_reader = stop_cross_platform_external_screen_reader
get_screen_reader = get_cross_platform_screen_reader

if __name__ == "__main__":
    # Test the cross-platform external screen reader
    print("Starting cross-platform external screen reader test...")
    reader = start_cross_platform_external_screen_reader()
    
    if reader:
        print("Screen reader started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_cross_platform_external_screen_reader()
            print("Screen reader stopped.")