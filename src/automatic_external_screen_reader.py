"""
Automatic External Screen Reader for AccessMate
Enhanced version that starts automatically with continuous mode enabled
"""

from dataclasses import dataclass
from src.cross_platform_external_screen_reader import (
    CrossPlatformExternalScreenReader,
    ScreenReaderConfig,
    start_cross_platform_external_screen_reader,
    stop_cross_platform_external_screen_reader
)

@dataclass
class AutomaticScreenReaderConfig(ScreenReaderConfig):
    """Configuration for automatic external screen reader"""
    auto_start_continuous: bool = True
    auto_start_enabled: bool = True
    focus_change_delay: float = 1.0
    auto_read_new_windows: bool = True
    auto_read_notifications: bool = True

class AutomaticExternalScreenReader(CrossPlatformExternalScreenReader):
    """Automatic version of the external screen reader that works continuously"""
    
    def __init__(self, config: AutomaticScreenReaderConfig = None):
        # Use automatic config by default
        config = config or AutomaticScreenReaderConfig()
        super().__init__(config)
        
        # Enable continuous mode immediately
        self.continuous_mode = True
        print("🤖 Automatic External Screen Reader initialized")
        print("   ✅ Continuous mode enabled by default")
        print("   ✅ Auto-reading window changes")
        print("   ✅ Background monitoring active")
    
    def start(self):
        """Start the automatic external screen reader"""
        if not self.dependencies_available:
            print(f"Cannot start automatic screen reader on {self.platform} - dependencies missing")
            return False
            
        self.is_running = True
        self.continuous_mode = True  # Force continuous mode
        
        print(f"🚀 Automatic External Screen Reader STARTED on {self.platform}")
        print("🔄 Continuous reading mode is ACTIVE")
        print("📱 Window changes will be announced automatically")
        
        # Announce the startup
        self._speak("Automatic screen reader started. I will now read window changes automatically.")
        
        # Start background monitoring
        self._start_automatic_monitoring()
        
        return True
    
    def _start_automatic_monitoring(self):
        """Start enhanced automatic monitoring"""
        import threading
        import time
        
        def automatic_monitor():
            print("🔍 Starting enhanced automatic monitoring...")
            last_window_title = None
            
            while self.is_running:
                try:
                    # Get current window info
                    current_window = self._get_active_window()
                    
                    if current_window:
                        window_title = str(current_window)
                        
                        # Check if window changed
                        if window_title != last_window_title:
                            last_window_title = window_title
                            print(f"📋 New window detected: {window_title}")
                            
                            # Automatically read the new window
                            if self.config.auto_read_new_windows:
                                self._auto_read_window(window_title)
                    
                    # Use configurable delay
                    time.sleep(self.config.focus_change_delay)
                    
                except Exception as e:
                    print(f"Automatic monitoring error: {e}")
                    time.sleep(2)
            
            print("🔍 Automatic monitoring stopped")
        
        # Start the monitoring thread
        monitor_thread = threading.Thread(target=automatic_monitor, daemon=True)
        monitor_thread.start()
        print("✅ Enhanced automatic monitoring thread started")
    
    def _auto_read_window(self, window_title):
        """Automatically read content from a new window"""
        try:
            # Get window text
            window_text = self._get_window_text()
            
            if window_text and len(window_text.strip()) > 0:
                # Announce the window change with content
                announcement = f"New window: {window_title}. Content: {window_text[:200]}"
                self._speak(announcement)
                print(f"📢 Auto-announced: {window_title}")
            else:
                # Just announce the window name
                self._speak(f"Switched to {window_title}")
                print(f"📢 Auto-announced window: {window_title}")
                
        except Exception as e:
            print(f"Error auto-reading window: {e}")
            # Fallback to just window title
            self._speak(f"Switched to {window_title}")

# Global automatic screen reader instance
_automatic_screen_reader = None

def start_automatic_external_screen_reader():
    """Start the automatic external screen reader"""
    global _automatic_screen_reader
    
    if _automatic_screen_reader and _automatic_screen_reader.is_running:
        print("Automatic external screen reader already running")
        return _automatic_screen_reader
    
    print("🚀 Starting Automatic External Screen Reader...")
    _automatic_screen_reader = AutomaticExternalScreenReader()
    success = _automatic_screen_reader.start()
    
    if success:
        print("✅ Automatic External Screen Reader started successfully!")
        print("🔄 Continuous mode is active - window changes will be announced automatically")
        return _automatic_screen_reader
    else:
        print("❌ Failed to start Automatic External Screen Reader")
        return None

def stop_automatic_external_screen_reader():
    """Stop the automatic external screen reader"""
    global _automatic_screen_reader
    
    if _automatic_screen_reader:
        _automatic_screen_reader.stop()
        _automatic_screen_reader = None
        print("🛑 Automatic External Screen Reader stopped")

def get_automatic_screen_reader():
    """Get the current automatic screen reader instance"""
    return _automatic_screen_reader

def is_automatic_screen_reader_running():
    """Check if automatic screen reader is running"""
    return _automatic_screen_reader and _automatic_screen_reader.is_running

# Test function
if __name__ == "__main__":
    print("Testing Automatic External Screen Reader...")
    reader = start_automatic_external_screen_reader()
    
    if reader:
        print("✅ Automatic screen reader started successfully!")
        print("Switch between different applications to test automatic reading...")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping automatic screen reader...")
            stop_automatic_external_screen_reader()
    else:
        print("❌ Failed to start automatic screen reader")