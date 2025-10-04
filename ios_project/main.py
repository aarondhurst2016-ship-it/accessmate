#!/usr/bin/env python3
"""
iOS version of AccessMate - Mobile-optimized accessibility assistant with welcome system
"""

import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    # Import the Android/mobile version which has welcome popup and voice setup
    from main_android import main
    
    print("AccessMate iOS - Starting with welcome system...")
    
    # Launch mobile app with welcome popup and voice setup
    main()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Running in fallback mode...")
    
    # Fallback iOS app if main_android import fails
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        class FallbackAccessMateApp(App):
            def build(self):
                layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
                
                title = Label(text='AccessMate iOS', font_size='20sp', size_hint_y=None, height='60dp')
                subtitle = Label(text='Accessibility Assistant', font_size='14sp', size_hint_y=None, height='40dp')
                
                info_btn = Button(text='About', size_hint_y=None, height='50dp')
                info_btn.bind(on_press=self.show_info)
                
                layout.add_widget(title)
                layout.add_widget(subtitle)
                layout.add_widget(info_btn)
                
                return layout
            
            def show_info(self, instance):
                print("AccessMate - Comprehensive accessibility assistant for iOS")
        
        FallbackAccessMateApp().run()
        
    except ImportError:
        # Ultimate fallback - basic console
        print("AccessMate iOS - Limited console mode")
        print("Welcome to AccessMate - Accessibility features available via voice commands")
        input("Press Enter to exit...")

if __name__ == "__main__":
    print("AccessMate iOS version starting with welcome system...")
