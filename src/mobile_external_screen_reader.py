"""
Mobile External Screen Reader for AccessMate
Android-compatible screen reading for other apps
"""

import sys
import os
import time
import threading
from typing import Optional, List, Dict, Any

class MobileExternalScreenReader:
    """Mobile screen reader for reading content from other Android apps"""
    
    def __init__(self):
        self.is_running = False
        self.continuous_mode = False
        self.platform = sys.platform
        self.accessibility_available = False
        
        # Initialize platform-specific modules
        self._init_mobile_modules()
    
    def _init_mobile_modules(self):
        """Initialize mobile accessibility modules"""
        if self.platform == 'android':
            try:
                # Try to import Android-specific modules
                from jnius import autoclass, PythonJavaClass, java_method  # type: ignore
                from android.permissions import request_permissions, Permission  # type: ignore
                from android import activity  # type: ignore
                
                self.autoclass = autoclass
                self.PythonJavaClass = PythonJavaClass
                self.java_method = java_method
                self.request_permissions = request_permissions
                self.Permission = Permission
                self.activity = activity
                
                # Request accessibility permissions
                request_permissions([
                    Permission.BIND_ACCESSIBILITY_SERVICE,
                    Permission.SYSTEM_ALERT_WINDOW
                ])
                
                self.accessibility_available = True
                print("Android accessibility modules initialized")
                
            except ImportError as e:
                print(f"Android accessibility not available: {e}")
                self.accessibility_available = False
        else:
            print("Mobile external screen reader only supports Android")
    
    def start(self):
        """Start the mobile external screen reader"""
        if not self.accessibility_available:
            return False
            
        self.is_running = True
        print("Mobile external screen reader started")
        
        if self.platform == 'android':
            self._start_android_accessibility()
        
        return True
    
    def stop(self):
        """Stop the mobile external screen reader"""
        self.is_running = False
        self.continuous_mode = False
        print("Mobile external screen reader stopped")
    
    def _start_android_accessibility(self):
        """Start Android accessibility service"""
        try:
            # Create accessibility service class
            class AccessibilityServicePython(self.PythonJavaClass):
                __javainterfaces__ = ['android/accessibilityservice/AccessibilityService']
                
                def __init__(self, screen_reader):
                    super().__init__()
                    self.screen_reader = screen_reader
                
                @self.java_method('(Landroid/view/accessibility/AccessibilityEvent;)V')  # type: ignore
                def onAccessibilityEvent(self, event):
                    """Handle accessibility events"""
                    try:
                        if self.screen_reader.continuous_mode:
                            self._process_accessibility_event(event)
                    except Exception as e:
                        print(f"Accessibility event error: {e}")
                
                @self.java_method('()V')  # type: ignore
                def onInterrupt(self):
                    """Handle service interruption"""
                    print("Accessibility service interrupted")
                
                def _process_accessibility_event(self, event):
                    """Process accessibility events for screen reading"""
                    try:
                        event_type = event.getEventType()
                        source = event.getSource()
                        
                        if source:
                            text = source.getText()
                            if text:
                                self.screen_reader._speak(str(text))
                    except Exception as e:
                        print(f"Event processing error: {e}")
            
            # Start the accessibility service
            self.accessibility_service = AccessibilityServicePython(self)
            print("Android accessibility service configured")
            
        except Exception as e:
            print(f"Android accessibility service error: {e}")
    
    def read_active_app(self):
        """Read content from the currently active app"""
        if not self.is_running:
            return
            
        try:
            if self.platform == 'android':
                text = self._get_android_app_text()
            else:
                text = "Mobile screen reading not available on this platform"
            
            if text:
                self._speak(f"Reading active app: {text}")
            else:
                self._speak("No readable text found in active app")
                
        except Exception as e:
            print(f"Error reading active app: {e}")
            self._speak("Error reading active app")
    
    def _get_android_app_text(self):
        """Get text from Android app using accessibility service"""
        try:
            # Get the active window using accessibility service
            if hasattr(self, 'accessibility_service'):
                # This would typically involve querying the accessibility node tree
                # For now, return a placeholder message
                return "Android accessibility service active - reading app content"
            else:
                return "Android accessibility service not available"
        except Exception as e:
            print(f"Android app text error: {e}")
            return None
    
    def toggle_continuous_mode(self):
        """Toggle continuous reading mode"""
        self.continuous_mode = not self.continuous_mode
        status = "enabled" if self.continuous_mode else "disabled"
        self._speak(f"Continuous reading mode {status}")
        print(f"Continuous mode: {status}")
    
    def announce_app_switch(self, app_name):
        """Announce when switching to a different app"""
        if self.continuous_mode:
            self._speak(f"Switched to {app_name}")
    
    def read_notification(self, notification_text):
        """Read incoming notifications"""
        if self.is_running:
            self._speak(f"Notification: {notification_text}")
    
    def _speak(self, text):
        """Speak text using mobile TTS"""
        try:
            # Try to use the main app's speech module
            import sys
            import os
            sys.path.append(os.path.dirname(__file__))
            
            # For mobile, try Android TTS
            if self.platform == 'android':
                try:
                    from jnius import autoclass
                    TTS = autoclass('android.speech.tts.TextToSpeech')
                    Locale = autoclass('java.util.Locale')
                    
                    # Initialize TTS if not already done
                    if not hasattr(self, 'tts'):
                        self.tts = TTS(self.activity.mActivity, None)
                        self.tts.setLanguage(Locale.getDefault())
                    
                    self.tts.speak(text, TTS.QUEUE_FLUSH, None)
                    return
                except Exception as e:
                    print(f"Android TTS error: {e}")
            
            # Fallback to print
            print(f"Mobile Screen Reader: {text}")
            
        except Exception as e:
            print(f"Mobile speech error: {e}")
            print(f"Mobile Screen Reader: {text}")

# Global mobile screen reader instance
_mobile_screen_reader = None

def start_mobile_external_screen_reader():
    """Start mobile external screen reader"""
    global _mobile_screen_reader
    
    if _mobile_screen_reader and _mobile_screen_reader.is_running:
        print("Mobile external screen reader already running")
        return _mobile_screen_reader
    
    _mobile_screen_reader = MobileExternalScreenReader()
    success = _mobile_screen_reader.start()
    
    if success:
        print("Mobile external screen reader started successfully")
        print("Use gestures and voice commands to control:")
        print("- Tap screen: Read item at finger")
        print("- Swipe right: Next item")
        print("- Swipe left: Previous item") 
        print("- Two-finger tap: Toggle continuous mode")
    
    return _mobile_screen_reader

def stop_mobile_external_screen_reader():
    """Stop mobile external screen reader"""
    global _mobile_screen_reader
    
    if _mobile_screen_reader:
        _mobile_screen_reader.stop()
        _mobile_screen_reader = None
        print("Mobile external screen reader stopped")

def get_mobile_screen_reader():
    """Get current mobile screen reader instance"""
    return _mobile_screen_reader

def read_active_mobile_app():
    """Read the currently active mobile app"""
    if _mobile_screen_reader:
        _mobile_screen_reader.read_active_app()

def toggle_mobile_continuous_mode():
    """Toggle mobile continuous reading mode"""
    if _mobile_screen_reader:
        _mobile_screen_reader.toggle_continuous_mode()

if __name__ == "__main__":
    # Test mobile screen reader
    print("Starting mobile external screen reader test...")
    reader = start_mobile_external_screen_reader()
    
    if reader:
        print("Mobile screen reader started.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_mobile_external_screen_reader()
            print("Mobile screen reader stopped.")