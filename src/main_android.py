# Android-compatible main entry point for AccessMate
# This version avoids Windows-specific imports that break on Android

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class AccessMateApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text='AccessMate\nAccessibility Assistant',
            font_size='24sp',
            text_align='center',
            halign='center'
        )
        
        # Welcome message
        welcome = Label(
            text='Welcome to AccessMate - your AI-powered accessibility companion!',
            font_size='16sp',
            text_align='center',
            halign='center'
        )
        
        # Feature buttons
        voice_btn = Button(
            text='Voice Commands',
            size_hint_y=None,
            height='48dp'
        )
        
        screen_reader_btn = Button(
            text='Screen Reader',
            size_hint_y=None,
            height='48dp'
        )
        
        object_recognition_btn = Button(
            text='Object Recognition',
            size_hint_y=None,
            height='48dp'
        )
        
        # Add widgets to layout
        layout.add_widget(title)
        layout.add_widget(welcome)
        layout.add_widget(voice_btn)
        layout.add_widget(screen_reader_btn)
        layout.add_widget(object_recognition_btn)
        
        return layout

def main():
    """Main entry point - platform-agnostic"""
    try:
        # Try to detect platform
        if hasattr(sys, 'platform'):
            platform = sys.platform
        else:
            platform = 'unknown'
            
        print(f"Starting AccessMate on {platform}")
        
        # On Android, use Kivy app
        if platform == 'android' or 'ANDROID_ROOT' in os.environ:
            print("Running Android version")
            AccessMateApp().run()
        else:
            # On desktop platforms, try to import the GUI module
            try:
                from gui import launch
                print("Running desktop version")
                launch()
            except ImportError:
                print("GUI module not available, running basic Kivy version")
                AccessMateApp().run()
                
    except Exception as e:
        print(f"Error starting AccessMate: {e}")
        # Fallback to basic Kivy app
        AccessMateApp().run()

if __name__ == '__main__':
    main()