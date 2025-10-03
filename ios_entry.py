#!/usr/bin/env python3
# ios_entry.py
# Entry point for AccessMate on iOS using Kivy

import sys
import os
import platform
import logging

# Configure logging for iOS debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Kivy imports - kivy-ios will handle these
    from kivy.app import App  # pyright: ignore[reportMissingImports]
    from kivy.uix.boxlayout import BoxLayout  # pyright: ignore[reportMissingImports]
    from kivy.uix.label import Label  # pyright: ignore[reportMissingImports]
    from kivy.logger import Logger  # pyright: ignore[reportMissingImports]
    
    # Import our mobile GUI
    from mobial.gui import TalkbackGUI
    
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    # Fallback for development/testing
    print(f"Import error: {e}")
    sys.exit(1)

class AccessMateApp(App):
    """Main AccessMate iOS application class."""
    
    title = "AccessMate"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("AccessMate iOS app initializing...")
        
    def build(self):
        """Build the main application interface."""
        try:
            logger.info("Building AccessMate iOS interface...")
            
            # Create the main GUI
            gui = TalkbackGUI()
            
            # Log successful initialization
            logger.info("AccessMate iOS interface built successfully")
            
            return gui
            
        except Exception as e:
            logger.error(f"Failed to build iOS interface: {e}")
            
            # Return a simple error interface
            from kivy.uix.label import Label
            return Label(
                text=f"AccessMate iOS Error:\n{str(e)}\n\nCheck logs for details.",
                text_size=(None, None),
                halign='center',
                valign='middle'
            )
    
    def on_start(self):
        """Called when the app starts."""
        logger.info("AccessMate iOS app started")
        Logger.info("AccessMate: iOS app started successfully")
    
    def on_stop(self):
        """Called when the app stops."""
        logger.info("AccessMate iOS app stopping")
        Logger.info("AccessMate: iOS app stopped")
    
    def on_pause(self):
        """Called when the app is paused (iOS backgrounding)."""
        logger.info("AccessMate iOS app paused")
        return True  # Return True to allow pausing
    
    def on_resume(self):
        """Called when the app resumes from pause."""
        logger.info("AccessMate iOS app resumed")

def main():
    """Main entry point for iOS app."""
    logger.info(f"Starting AccessMate on iOS (Python {sys.version})")
    logger.info(f"Platform: {platform.platform()}")
    
    try:
        # Create and run the app
        app = AccessMateApp()
        app.run()
        
    except Exception as e:
        logger.error(f"Fatal error running AccessMate iOS app: {e}")
        raise

if __name__ == "__main__":
    main()
