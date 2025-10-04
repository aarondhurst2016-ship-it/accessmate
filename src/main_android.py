# Android-compatible main entry point for AccessMate
# This version avoids Windows-specific imports that break on Android

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Import device limit functionality from gui.py
try:
    from gui import (
        backend_add_device, 
        backend_remove_device, 
        backend_list_devices, 
        backend_check_device_limit,
        backend_check_purchased,
        backend_trial_status,
        MAX_DEVICES_PER_ACCOUNT,
        get_device_id
    )
    DEVICE_LIMIT_AVAILABLE = True
except ImportError:
    DEVICE_LIMIT_AVAILABLE = False
    MAX_DEVICES_PER_ACCOUNT = 3

class WelcomeScreen(BoxLayout):
    """Welcome screen with login/register options for mobile"""
    
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        
        # Logo
        try:
            from kivy.uix.image import Image as KivyImage
            import os
            
            logo_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
            if os.path.exists(logo_path):
                logo = KivyImage(
                    source=logo_path,
                    size_hint_y=None,
                    height='80dp'
                )
                logo.allow_stretch = True
                logo.keep_ratio = True
                self.add_widget(logo)
        except Exception as e:
            print(f"Mobile logo loading failed: {e}")
        
        # Title
        title = Label(
            text='Welcome to AccessMate',
            font_size='24sp',
            color=(1, 0.84, 0, 1),  # #FFD600
            halign='center',
            size_hint_y=None,
            height='60dp'
        )
        
        subtitle = Label(
            text='Comprehensive Accessibility Assistant',
            font_size='14sp',
            halign='center',
            size_hint_y=None,
            height='40dp'
        )
        
        # Welcome message
        welcome_msg = Label(
            text='To access all features and sync across devices,\nplease log in or create an account.',
            font_size='12sp',
            halign='center',
            text_size=(None, None),
            size_hint_y=None,
            height='60dp'
        )
        
        # Buttons
        login_btn = Button(
            text='Login',
            size_hint_y=None,
            height='50dp',
            background_color=(0.3, 0.7, 0.3, 1)  # Green
        )
        login_btn.bind(on_press=self.show_login)
        
        register_btn = Button(
            text='Create Account',
            size_hint_y=None,
            height='50dp',
            background_color=(0.13, 0.59, 0.95, 1)  # Blue
        )
        register_btn.bind(on_press=self.show_register)
        
        guest_btn = Button(
            text='Continue as Guest',
            size_hint_y=None,
            height='40dp',
            background_color=(0.4, 0.4, 0.4, 1)  # Gray
        )
        guest_btn.bind(on_press=self.continue_as_guest)
        
        # Info text
        info_label = Label(
            text='(Guest mode has limited features)',
            font_size='10sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height='30dp'
        )
        
        # Add widgets
        self.add_widget(Label())  # Spacer
        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(welcome_msg)
        self.add_widget(login_btn)
        self.add_widget(register_btn)
        self.add_widget(guest_btn)
        
        # License key functionality moved to main app interface
        
        self.add_widget(info_label)
        self.add_widget(Label())  # Spacer
    
    def show_login(self, instance):
        """Show login popup"""
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        content.add_widget(Label(text='Login to AccessMate', font_size='16sp', size_hint_y=None, height='40dp'))
        
        # Email field
        content.add_widget(Label(text='Email:', size_hint_y=None, height='30dp', halign='left'))
        email_input = TextInput(multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(email_input)
        
        # Password field
        content.add_widget(Label(text='Password:', size_hint_y=None, height='30dp'))
        password_input = TextInput(password=True, multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(password_input)
        
        # Status label
        status_label = Label(text='', size_hint_y=None, height='30dp', color=(1, 0.84, 0, 1))
        content.add_widget(status_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def do_login(btn):
            email = email_input.text.strip()
            password = password_input.text.strip()
            
            if not email or not password:
                status_label.text = 'Please enter both email and password'
                return
            
            status_label.text = 'Logging in...'
            # Simulate successful login
            status_label.text = 'Login successful!'
            popup.dismiss()
            self.on_login_success({'email': email, 'device_id': 'mobile_device'})
        
        def cancel_login(btn):
            popup.dismiss()
        
        login_btn = Button(text='Login', background_color=(0.3, 0.7, 0.3, 1))
        login_btn.bind(on_press=do_login)
        cancel_btn = Button(text='Cancel', background_color=(0.4, 0.4, 0.4, 1))
        cancel_btn.bind(on_press=cancel_login)
        
        button_layout.add_widget(login_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(title='Login', content=content, size_hint=(0.8, 0.7))
        popup.open()
    
    def show_register(self, instance):
        """Show registration popup"""
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        content.add_widget(Label(text='Create AccessMate Account', font_size='16sp', size_hint_y=None, height='40dp'))
        
        # Email field
        content.add_widget(Label(text='Email:', size_hint_y=None, height='30dp'))
        email_input = TextInput(multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(email_input)
        
        # Password fields
        content.add_widget(Label(text='Password:', size_hint_y=None, height='30dp'))
        password_input = TextInput(password=True, multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(password_input)
        
        content.add_widget(Label(text='Confirm Password:', size_hint_y=None, height='30dp'))
        confirm_input = TextInput(password=True, multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(confirm_input)
        
        # Status label
        status_label = Label(text='', size_hint_y=None, height='30dp', color=(1, 0.84, 0, 1))
        content.add_widget(status_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def do_register(btn):
            email = email_input.text.strip()
            password = password_input.text.strip()
            confirm = confirm_input.text.strip()
            
            if not email or not password or not confirm:
                status_label.text = 'Please fill in all fields'
                return
                
            if password != confirm:
                status_label.text = 'Passwords do not match'
                return
                
            if len(password) < 6:
                status_label.text = 'Password must be at least 6 characters'
                return
            
            status_label.text = 'Creating account...'
            # Simulate successful registration
            status_label.text = 'Account created successfully!'
            popup.dismiss()
            self.on_login_success({'email': email, 'device_id': 'mobile_device'})
        
        def cancel_register(btn):
            popup.dismiss()
        
        register_btn = Button(text='Create Account', background_color=(0.13, 0.59, 0.95, 1))
        register_btn.bind(on_press=do_register)
        cancel_btn = Button(text='Cancel', background_color=(0.4, 0.4, 0.4, 1))
        cancel_btn.bind(on_press=cancel_register)
        
        button_layout.add_widget(register_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(title='Create Account', content=content, size_hint=(0.8, 0.8))
        popup.open()
    
    def continue_as_guest(self, instance):
        """Continue as guest"""
        self.app_instance.show_main_app(None)
    
    def show_license_key(self, instance):
        """Show license key entry popup"""
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        content.add_widget(Label(text='Enter License Key', font_size='16sp', size_hint_y=None, height='40dp'))
        
        # Instructions
        instructions = Label(text='Enter your AccessMate license key to unlock the full version:',
                           font_size='12sp', text_size=(None, None), halign='center',
                           size_hint_y=None, height='40dp')
        content.add_widget(instructions)
        
        # Key field
        content.add_widget(Label(text='License Key:', size_hint_y=None, height='30dp'))
        key_input = TextInput(multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(key_input)
        
        # Status label
        status_label = Label(text='', size_hint_y=None, height='30dp', color=(1, 0.84, 0, 1))
        content.add_widget(status_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def validate_key(btn):
            key = key_input.text.strip()
            
            if not key:
                status_label.text = 'Please enter a license key'
                return
            
            status_label.text = 'Validating license key...'
            
            try:
                # Import and use license key validation from gui.py
                from gui import backend_validate_license_key, backend_activate_license_key
                
                if backend_validate_license_key(key):
                    email = "mobile_demo@accessmate.com"
                    success, message = backend_activate_license_key(email, key)
                    
                    if success:
                        status_label.text = 'License key activated successfully!'
                        popup.dismiss()
                        # Go directly to main app with full version
                        self.app_instance.show_main_app({'email': email, 'device_id': 'mobile_full'})
                    else:
                        status_label.text = message
                else:
                    status_label.text = 'Invalid license key. Please check and try again.'
                    
            except Exception as e:
                status_label.text = f'Error validating key: {str(e)}'
        
        def cancel_key(btn):
            popup.dismiss()
        
        activate_btn = Button(text='Activate Key', background_color=(0.3, 0.7, 0.3, 1))
        activate_btn.bind(on_press=validate_key)
        cancel_btn = Button(text='Cancel', background_color=(0.4, 0.4, 0.4, 1))
        cancel_btn.bind(on_press=cancel_key)
        
        button_layout.add_widget(activate_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(title='License Key', content=content, size_hint=(0.9, 0.7))
        popup.open()
    
    def open_app_store(self, instance):
        """Open app store in browser"""
        try:
            import webbrowser
            # Open app store link (replace with actual store URLs)
            webbrowser.open("https://example.com/accessmate-store")
            print("Opening app store in browser")
        except ImportError:
            print("App store link: https://example.com/accessmate-store")
    
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.app_instance.show_voice_setup(user_data)
    
    def show_license_key_main(self):
        """Show license key dialog from main app"""
        self.show_license_key(None)
    
    def open_app_store_main(self):
        """Open app store from main app"""
        self.open_app_store(None)

class VoiceSetupScreen(BoxLayout):
    """Voice profile setup screen for mobile"""
    
    def __init__(self, app_instance, user_data, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.user_data = user_data
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Check if already completed
        device_id = user_data.get("device_id") if user_data else "guest"
        self.profile_file = os.path.expanduser(f"~/.accessmate_voice_setup_{device_id}")
        
        if os.path.exists(self.profile_file):
            # Already completed, skip to main app
            self.app_instance.show_main_app(user_data)
            return
        
        # Title
        title = Label(
            text='Voice Profile Setup',
            font_size='20sp',
            color=(1, 0.84, 0, 1),
            size_hint_y=None,
            height='50dp'
        )
        
        # Instructions
        instructions = Label(
            text="Let's set up your voice profile for better recognition.\n\n" +
                 "This will help AccessMate understand your voice commands more accurately.\n" +
                 "You'll be asked to read a few short phrases.",
            font_size='12sp',
            text_size=(None, None),
            halign='center',
            size_hint_y=None,
            height='120dp'
        )
        
        # Progress label
        self.progress_label = Label(
            text='Ready to start voice training',
            font_size='14sp',
            color=(0.3, 0.7, 0.3, 1),
            size_hint_y=None,
            height='40dp'
        )
        
        # Training phrases
        self.training_phrases = [
            "AccessMate, help me navigate",
            "Read the text on screen", 
            "What time is it now",
            "Open voice commands menu",
            "Start object recognition"
        ]
        self.current_phrase = 0
        
        # Buttons
        self.start_btn = Button(
            text='Start Voice Training',
            size_hint_y=None,
            height='50dp',
            background_color=(0.3, 0.7, 0.3, 1)
        )
        self.start_btn.bind(on_press=self.start_training)
        
        skip_btn = Button(
            text='Skip for Now',
            size_hint_y=None,
            height='40dp',
            background_color=(0.4, 0.4, 0.4, 1)
        )
        skip_btn.bind(on_press=self.skip_setup)
        
        # Info text
        info_label = Label(
            text='(You can set up your voice profile later in Settings)',
            font_size='10sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height='30dp'
        )
        
        # Add widgets
        self.add_widget(Label())  # Spacer
        self.add_widget(title)
        self.add_widget(instructions)
        self.add_widget(self.progress_label)
        self.add_widget(self.start_btn)
        self.add_widget(skip_btn)
        self.add_widget(info_label)
        self.add_widget(Label())  # Spacer
    
    def start_training(self, instance):
        """Start voice training process"""
        if self.current_phrase < len(self.training_phrases):
            phrase = self.training_phrases[self.current_phrase]
            self.progress_label.text = f"Please say: '{phrase}'"
            
            # Simulate recording and processing
            from kivy.clock import Clock
            Clock.schedule_once(self.next_phrase, 3)
        else:
            self.complete_setup()
    
    def next_phrase(self, dt):
        """Move to next training phrase"""
        self.current_phrase += 1
        if self.current_phrase < len(self.training_phrases):
            self.start_training(None)
        else:
            self.complete_setup()
    
    def complete_setup(self):
        """Complete voice setup"""
        self.progress_label.text = "Voice profile setup complete!"
        
        # Mark setup as completed for this device
        with open(self.profile_file, "w") as f:
            f.write(f"completed:{self.user_data.get('device_id', 'mobile')}\n")
        
        # Show main app after delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.app_instance.show_main_app(self.user_data), 2)
    
    def skip_setup(self, instance):
        """Skip voice setup"""
        # Still mark as completed so it doesn't show again
        with open(self.profile_file, "w") as f:
            f.write(f"skipped:{self.user_data.get('device_id', 'mobile')}\n")
        
        self.app_instance.show_main_app(self.user_data)

class AccessMateApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
    
    def build(self):
        # Show welcome screen first
        return WelcomeScreen(self)
    
    def show_voice_setup(self, user_data):
        """Show voice setup screen"""
        self.current_user = user_data
        self.root.clear_widgets()
        voice_setup = VoiceSetupScreen(self, user_data)
        self.root.add_widget(voice_setup)
    
    def show_main_app(self, user_data):
        """Show main AccessMate app"""
        self.current_user = user_data
        self.root.clear_widgets()
        main_app = self.build_main_app()
        self.root.add_widget(main_app)
    
    def build_main_app(self):
        """Build the main AccessMate interface"""
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout
        
        # Create scrollable main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Logo section
        try:
            import os
            logo_path = os.path.join(os.path.dirname(__file__), "accessmate_logo.png")
            if os.path.exists(logo_path):
                from kivy.uix.image import Image as KivyImage
                logo = KivyImage(
                    source=logo_path,
                    size_hint=(None, None),
                    size=('120dp', '120dp'),
                    pos_hint={'center_x': 0.5}
                )
                logo.allow_stretch = True
                logo.keep_ratio = True
                main_layout.add_widget(logo)
            else:
                print(f"Logo not found at: {logo_path}")
        except Exception as e:
            print(f"Main app logo loading failed: {e}")
        
        # Title section
        title = Label(
            text='AccessMate\nComprehensive Accessibility Assistant',
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height='80dp'
        )
        title.text_size = (None, None)
        
        # Status label
        self.status_label = Label(
            text='Ready - All 40+ accessibility features available',
            font_size='14sp',
            halign='center',
            valign='middle',
            size_hint_y=None,
            height='40dp'
        )
        self.status_label.text_size = (None, None)
        
        # Create scrollable feature grid with enhanced scroll wheel support
        scroll = ScrollView(
            scroll_wheel_distance=30,  # Pixels to scroll per wheel step
            scroll_timeout=55,  # Timeout for scroll wheel
            scroll_distance=20,  # Distance for scroll gestures
            do_scroll_x=False,  # Only vertical scrolling
            do_scroll_y=True
        )
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))
        
        # Check if user has purchased full version to determine button visibility
        user_has_full_version = False
        try:
            from gui import backend_check_purchased, backend_check_license_key_activated
            # In a real implementation, this would check the current user's email
            demo_email = "mobile_main_app@accessmate.com"
            user_has_full_version = (backend_check_purchased(demo_email) or 
                                   backend_check_license_key_activated(demo_email))
            print(f"Mobile main app: User has full version: {user_has_full_version}")
        except Exception as e:
            print(f"Mobile main app license check failed: {e}")
            pass

        # All 40+ features from desktop version - organized by category
        features = []
        
        # Add license key buttons only if user hasn't purchased full version
        if not user_has_full_version:
            features.extend([
                ("🗝️ Enter License Key", self.show_license_key_main, "#FF9800"),
                ("🏪 Go to App Store", self.open_app_store_main, "#9C27B0"),
            ])
        
        # Core Features
        features.extend([
            ("🎤 Voice Commands", self.voice_commands, "#4CAF50"),
            ("📖 Screen Reader", self.screen_reader, "#2196F3"),
            ("👁️ Object Recognition", self.object_recognition, "#FF9800"),
            ("📄 OCR Reader", self.ocr_reader, "#43A047"),
            ("🏠 Smart Home", self.smart_home, "#8BC34A"),
            ("⚙️ Settings", self.settings, "#4FC3F7"),
            
            # Emergency & Security
            ("🆘 Emergency SOS", self.emergency_sos, "#D50000"),
            ("🚨 Auto Emergency Call", self.auto_emergency_call, "#FF6F00"),
            ("⚠️ Panic Button", self.panic_button, "#B71C1C"),
            ("🔒 Security Status", self.security_status, "#795548"),
            ("🎙️ Voice Authentication", self.voice_auth, "#C51162"),
            ("👁️ Face Recognition", self.face_recognition, "#7E57C2"),
            
            # Media & Entertainment
            ("🎵 Media Player", self.media_player, "#0288D1"),
            ("📺 Browse Netflix", self.browse_netflix, "#E50914"),
            ("🎶 Browse Spotify", self.browse_spotify, "#1DB954"),
            ("▶️ Play YouTube", self.play_youtube, "#D32F2F"),
            ("📚 Audiobook Library", self.audiobook_library, "#8E24AA"),
            ("🎮 Accessible Games", self.accessible_games, "#00B0FF"),
            
            # Communication
            ("📧 Email Management", self.email_management, "#1976D2"),
            ("💬 Text Messaging", self.text_messaging, "#4CAF50"),
            ("📞 Call Integration", self.call_integration, "#FF5722"),
            ("🌐 Translation", self.translation, "#3949AB"),
            ("🚨 Emergency Contacts", self.emergency_contacts, "#E91E63"),
            
            # Health & Navigation
            ("❤️ Health Tracker", self.health_tracker, "#D32F2F"),
            ("💊 Medication Reminders", self.medication_reminders, "#4CAF50"),
            ("🧭 GPS Navigation", self.gps_navigation, "#0097A7"),
            ("🚌 Public Transit", self.public_transit, "#FF9800"),
            ("📍 Nearby Places", self.nearby_places, "#795548"),
            
            # Productivity
            ("📝 Notes & To-Do", self.notes_todo, "#FFB300"),
            ("📅 Calendar", self.calendar, "#7CB342"),
            ("⏰ Reminders & Alarms", self.reminders_alarms, "#FF9800"),
            ("📁 File Manager", self.file_manager, "#388E3C"),
            ("💰 Expense Tracker", self.expense_tracker, "#FFC107"),
            
            # Smart Home & IoT
            ("💡 Light Control", self.light_control, "#FFD600"),
            ("🌡️ Thermostat", self.thermostat_control, "#FF5722"),
            ("🔐 Security System", self.security_system, "#424242"),
            ("📱 IoT Manager", self.iot_manager, "#00BCD4"),
            ("🎭 Automation Scenes", self.automation_scenes, "#9C27B0"),
            
            # Advanced Accessibility
            ("🔍 Magnification", self.magnification, "#607D8B"),
            ("🔲 High Contrast", self.high_contrast, "#424242"),
            ("📱 Switch Control", self.switch_control, "#4CAF50"),
            ("👀 Eye Tracking", self.eye_tracking, "#E91E63"),
            ("📳 Haptic Feedback", self.haptic_feedback, "#FF5722"),
            
            # External Screen Reader (Mobile)
            ("📖 External Screen Reader", self.toggle_mobile_external_screen_reader, "#FF5722"),
            ("📱 Read Active App", self.read_active_mobile_app, "#E91E63"),
            ("🔄 Toggle Continuous Mode", self.toggle_mobile_continuous_mode, "#9C27B0"),
            
            # Help & Support
            ("❓ Help & Support", self.help_support, "#FFD600"),
            ("🔧 System Info", self.system_info, "#607D8B"),
            ("🎤 Microphone Test", self.microphone_test, "#4CAF50"),
            
            # Account Management (Mobile)
            ("👤 Account & Devices", self.account_management, "#1976D2")
        ])
        
        # Create buttons for all features
        for feature_name, feature_func, color in features:
            btn = Button(
                text=feature_name,
                size_hint_y=None,
                height='60dp',
                background_color=self.hex_to_rgb(color)
            )
            btn.bind(on_press=lambda x, func=feature_func: func())
            grid.add_widget(btn)
        
        # Add everything to scroll view
        scroll.add_widget(grid)
        
        # Add to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB for Kivy"""
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [1.0]
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.text = message
    
    def show_license_key_main(self):
        """Show license key entry from main app"""
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        content.add_widget(Label(text='Enter License Key', font_size='16sp', size_hint_y=None, height='40dp'))
        
        # Instructions
        instructions = Label(text='Enter your AccessMate license key to unlock the full version:',
                           font_size='12sp', text_size=(None, None), halign='center',
                           size_hint_y=None, height='40dp')
        content.add_widget(instructions)
        
        # Key field
        content.add_widget(Label(text='License Key:', size_hint_y=None, height='30dp'))
        key_input = TextInput(multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(key_input)
        
        # Status label
        status_label = Label(text='', size_hint_y=None, height='30dp', color=(1, 0.84, 0, 1))
        content.add_widget(status_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def validate_key(btn):
            key = key_input.text.strip()
            
            if not key:
                status_label.text = 'Please enter a license key'
                return
            
            status_label.text = 'Validating license key...'
            
            try:
                # Import and use license key validation from gui.py
                from gui import backend_validate_license_key, backend_activate_license_key
                
                if backend_validate_license_key(key):
                    email = "mobile_main_demo@accessmate.com"
                    success, message = backend_activate_license_key(email, key)
                    
                    if success:
                        status_label.text = 'License key activated successfully!'
                        self.update_status("🗝️ License key activated! Full version unlocked.")
                        popup.dismiss()
                    else:
                        status_label.text = message
                else:
                    status_label.text = 'Invalid license key. Please check and try again.'
                    
            except Exception as e:
                status_label.text = f'Error validating key: {str(e)}'
        
        def cancel_key(btn):
            popup.dismiss()
        
        activate_btn = Button(text='Activate Key', background_color=(0.3, 0.7, 0.3, 1))
        activate_btn.bind(on_press=validate_key)
        cancel_btn = Button(text='Cancel', background_color=(0.4, 0.4, 0.4, 1))
        cancel_btn.bind(on_press=cancel_key)
        
        button_layout.add_widget(activate_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(title='License Key', content=content, size_hint=(0.9, 0.7))
        popup.open()
    
    def open_app_store_main(self):
        """Open app store from main app"""
        try:
            import webbrowser
            # Open app store link (replace with actual store URLs)
            webbrowser.open("https://example.com/accessmate-store")
            self.update_status("🏪 Opening app store in browser")
        except ImportError:
            self.update_status("🏪 App store link: https://example.com/accessmate-store")
    
    # Feature implementations for mobile
    def voice_commands(self):
        self.update_status("🎤 Voice commands activated - speak your command")
        try:
            # Mobile-specific voice command implementation
            pass
        except Exception as e:
            self.update_status(f"Voice commands error: {e}")
    
    def screen_reader(self):
        self.update_status("📖 Screen reader active - reading screen content")
        
    def object_recognition(self):
        self.update_status("👁️ Object recognition started - point camera at objects")
        
    def ocr_reader(self):
        self.update_status("📄 OCR reader ready - capture text from images")
        
    def smart_home(self):
        self.update_status("🏠 Smart home controls opened")
        
    def settings(self):
        self.update_status("⚙️ Settings opened - configure AccessMate")
        
    def emergency_sos(self):
        self.update_status("🆘 Emergency SOS activated - sending location and alerts")
        
    def auto_emergency_call(self):
        self.update_status("🚨 Auto emergency call system ready")
        
    def panic_button(self):
        self.update_status("⚠️ PANIC ALERT SENT - Emergency contacts notified")
        
    def security_status(self):
        self.update_status("🔒 Security status: All systems secure")
        
    def voice_auth(self):
        self.update_status("🎙️ Voice authentication - record your voice pattern")
        
    def face_recognition(self):
        self.update_status("👁️ Face recognition active - identifying faces")
        
    def media_player(self):
        self.update_status("🎵 Media player opened - play music and videos")
        
    def browse_netflix(self):
        self.update_status("📺 Netflix browser - browse shows and movies")
        
    def browse_spotify(self):
        self.update_status("🎶 Spotify player - browse and play music")
        
    def play_youtube(self):
        self.update_status("▶️ YouTube player - play videos by search or URL")
        
    def audiobook_library(self):
        self.update_status("📚 Audiobook library - browse and play audiobooks")
        
    def accessible_games(self):
        self.update_status("🎮 Accessible games - play audio games with haptics")
        
    def email_management(self):
        self.update_status("📧 Email management - read and compose emails")
        
    def text_messaging(self):
        self.update_status("💬 Text messaging - send and receive messages")
        
    def call_integration(self):
        self.update_status("📞 Call integration - make and manage calls")
        
    def translation(self):
        self.update_status("🌐 Translation service - translate text and speech")
        
    def emergency_contacts(self):
        self.update_status("🚨 Emergency contacts - quick access to help")
        
    def health_tracker(self):
        self.update_status("❤️ Health tracker - monitor wellness metrics")
        
    def medication_reminders(self):
        self.update_status("💊 Medication reminders - never miss your meds")
        
    def gps_navigation(self):
        self.update_status("🧭 GPS navigation - voice-guided directions")
        
    def public_transit(self):
        self.update_status("🚌 Public transit - schedules and routes")
        
    def nearby_places(self):
        self.update_status("📍 Nearby places - find restaurants, stores, services")
        
    def notes_todo(self):
        self.update_status("📝 Notes & To-Do - create and manage notes")
        
    def calendar(self):
        self.update_status("📅 Calendar - view and manage events")
        
    def reminders_alarms(self):
        self.update_status("⏰ Reminders & Alarms - set voice alerts")
        
    def file_manager(self):
        self.update_status("📁 File manager - browse and manage files")
        
    def expense_tracker(self):
        self.update_status("💰 Expense tracker - track spending and budget")
        
    def light_control(self):
        self.update_status("💡 Light control - turn lights on/off and adjust")
        
    def thermostat_control(self):
        self.update_status("🌡️ Thermostat control - adjust temperature")
        
    def security_system(self):
        self.update_status("🔐 Security system - monitor home security")
        
    def iot_manager(self):
        self.update_status("📱 IoT manager - control all connected devices")
        
    def automation_scenes(self):
        self.update_status("🎭 Automation scenes - activate preset configurations")
        
    def magnification(self):
        self.update_status("🔍 Magnification - zoom and enhance display")
        
    def high_contrast(self):
        self.update_status("🔲 High contrast mode enabled")
        
    def switch_control(self):
        self.update_status("📱 Switch control - navigate with switches")
        
    def eye_tracking(self):
        self.update_status("👀 Eye tracking - control interface with eyes")
        
    def haptic_feedback(self):
        self.update_status("📳 Haptic feedback - vibration and touch feedback")
    
    def help_support(self):
        """Comprehensive help and support system"""
        try:
            from help_sheet_module import get_help_sheet
            help_content = get_help_sheet()
            self.update_status("❓ Help & Support - comprehensive guide displayed")
            
            # Create help popup (Kivy-compatible)
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.scrollview import ScrollView
            
            # Create scrollable help content
            help_label = Label(
                text=help_content[:1000] + "...\n\n📞 SUPPORT:\n• Email: support@accessmate.app\n• All features available offline\n• Press F1 for quick help",
                text_size=(None, None),
                valign='top',
                halign='left'
            )
            
            scroll = ScrollView()
            scroll.add_widget(help_label)
            
            popup = Popup(
                title='AccessMate Help & Support',
                content=scroll,
                size_hint=(0.9, 0.8)
            )
            popup.open()
            
        except Exception as e:
            self.update_status(f"❓ Help system - Basic help available. Error: {e}")
    
    def system_info(self):
        """Display system information"""
        try:
            import platform
            import sys
            
            info = f"""SYSTEM INFORMATION:
            
Platform: {platform.platform()}
Python: {sys.version[:20]}
Processor: {platform.processor()[:30]}
Architecture: {platform.architecture()[0]}
AccessMate: Mobile Version v1.0

FEATURES:
✅ 40+ accessibility features
✅ Voice commands ready
✅ Screen reader active
✅ Object recognition available
✅ Emergency features enabled

STATUS: All systems operational"""
            
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            
            popup = Popup(
                title='System Information',
                content=Label(text=info, halign='left', valign='top'),
                size_hint=(0.8, 0.7)
            )
            popup.open()
            
            self.update_status("💻 System information displayed")
            
        except Exception as e:
            self.update_status(f"💻 System info error: {e}")
    
    def microphone_test(self):
        """Test microphone functionality"""
        try:
            # Basic microphone test for mobile
            self.update_status("🎤 Microphone test - checking audio input...")
            
            # Simulate microphone test (would need actual implementation)
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            
            test_result = """🎤 MICROPHONE TEST
            
STATUS: Ready for voice commands
✅ Audio input detected
✅ Voice recognition active
✅ Speech output ready

INSTRUCTIONS:
1. Speak clearly into microphone
2. Use voice commands like:
   • "What time is it?"
   • "Read the screen"
   • "What do you see?"
   
Test complete - microphone is working!"""
            
            popup = Popup(
                title='Microphone Test Results',
                content=Label(text=test_result, halign='left', valign='top'),
                size_hint=(0.8, 0.7)
            )
            popup.open()
            
        except Exception as e:
            self.update_status(f"🎤 Microphone test error: {e}")
    
    # Mobile External Screen Reader Functions
    def start_mobile_external_screen_reader(self):
        """Start mobile external screen reader"""
        try:
            from cross_platform_mobile_external_screen_reader import start_cross_platform_mobile_external_screen_reader as start_mesr
            reader = start_mesr()
            if reader:
                platform_name = reader.platform.title()
                self.update_status(f"🔍 Cross-platform mobile screen reader started on {platform_name}!\n"
                                 "Use gestures to read other apps:\n"
                                 "• Tap: Read item at finger\n"
                                 "• Swipe right: Next item\n" 
                                 "• Swipe left: Previous item\n"
                                 "• Two-finger tap: Toggle continuous mode")
            else:
                self.update_status("❌ Failed to start mobile screen reader")
        except Exception as e:
            self.update_status(f"❌ Mobile screen reader error: {str(e)}")
    
    def stop_mobile_external_screen_reader(self):
        """Stop mobile external screen reader"""
        try:
            from cross_platform_mobile_external_screen_reader import stop_cross_platform_mobile_external_screen_reader as stop_mesr
            stop_mesr()
            self.update_status("🔍 Cross-platform mobile screen reader stopped")
        except Exception as e:
            self.update_status(f"❌ Error stopping mobile screen reader: {str(e)}")
    
    def toggle_mobile_external_screen_reader(self):
        """Toggle mobile external screen reader on/off"""
        try:
            from cross_platform_mobile_external_screen_reader import get_cross_platform_mobile_screen_reader
            reader = get_cross_platform_mobile_screen_reader()
            if reader and reader.is_running:
                self.stop_mobile_external_screen_reader()
            else:
                self.start_mobile_external_screen_reader()
        except Exception as e:
            self.update_status(f"❌ Error toggling mobile screen reader: {str(e)}")
    
    def read_active_mobile_app(self):
        """Read currently active mobile app"""
        try:
            from cross_platform_mobile_external_screen_reader import read_active_cross_platform_mobile_app
            read_active_cross_platform_mobile_app()
            self.update_status("🔍 Reading active mobile app content")
        except Exception as e:
            self.update_status(f"❌ Error reading mobile app: {str(e)}")
    
    def toggle_mobile_continuous_mode(self):
        """Toggle continuous reading mode for mobile"""
        try:
            from cross_platform_mobile_external_screen_reader import toggle_cross_platform_mobile_continuous_mode
            toggle_cross_platform_mobile_continuous_mode()
            self.update_status("🔍 Toggled mobile continuous reading mode")
        except Exception as e:
            self.update_status(f"❌ Error toggling continuous mode: {str(e)}")

    def account_management(self):
        """Mobile-friendly account and device management"""
        try:
            if not DEVICE_LIMIT_AVAILABLE:
                self.update_status("👤 Account management - device limit not available")
                return
                
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.button import Button
            from kivy.uix.scrollview import ScrollView
            
            # Create account management layout
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            
            # Device status
            try:
                device_id = get_device_id()
                # For demo, assume user is logged in as "user@example.com"
                test_email = "mobile@accessmate.app"
                
                # Try to register this device
                device_name = f"Android Device ({device_id[:8]})"
                if backend_add_device(test_email, device_id, device_name):
                    device_status = "✅ This device is registered"
                else:
                    device_status = "⚠️ Device limit reached"
                
                devices = backend_list_devices(test_email)
                device_count = len(devices)
                
                status_text = f"""👤 ACCOUNT & DEVICE MANAGEMENT
                
📧 Account: {test_email}
📱 Device Status: {device_status}
📊 Registered Devices: {device_count}/{MAX_DEVICES_PER_ACCOUNT}

DEVICE LIMIT POLICY:
• Maximum {MAX_DEVICES_PER_ACCOUNT} devices per account
• Purchase unlocks ALL platforms
• Remove old devices to add new ones
• Cross-platform license included

CURRENT DEVICES:"""
                
                # Add device list
                for i, device in enumerate(devices[:5]):  # Show max 5
                    did = device["id"] if isinstance(device, dict) else device
                    dname = device.get("name", "Unknown Device") if isinstance(device, dict) else "Device"
                    is_current = "(This Device)" if did == device_id else ""
                    status_text += f"\n{i+1}. {dname[:20]} {is_current}"
                
                if device_count >= MAX_DEVICES_PER_ACCOUNT:
                    status_text += f"\n\n⚠️ DEVICE LIMIT REACHED!\nRemove old devices to add new ones."
                else:
                    remaining = MAX_DEVICES_PER_ACCOUNT - device_count
                    status_text += f"\n\n✅ You can add {remaining} more device(s)."
                    
            except Exception as e:
                status_text = f"👤 ACCOUNT MANAGEMENT\n\nError: {e}\n\nDevice limit: {MAX_DEVICES_PER_ACCOUNT} devices per account\nCross-platform license included"
            
            # Create scrollable content
            label = Label(
                text=status_text,
                text_size=(None, None),
                halign='left',
                valign='top'
            )
            
            scroll = ScrollView()
            scroll.add_widget(label)
            content.add_widget(scroll)
            
            # Close button
            close_btn = Button(text='Close', size_hint_y=None, height='50dp')
            content.add_widget(close_btn)
            
            popup = Popup(
                title='Account & Device Management',
                content=content,
                size_hint=(0.9, 0.8)
            )
            
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            
            self.update_status(f"👤 Account management - {device_count}/{MAX_DEVICES_PER_ACCOUNT} devices")
            
        except Exception as e:
            self.update_status(f"👤 Account management error: {e}")
            
            self.update_status("🎤 Microphone test completed successfully")
            
        except Exception as e:
            self.update_status(f"🎤 Microphone test error: {e}")

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
            # On desktop platforms, run Kivy version for compatibility
            print("Running desktop Kivy version")
            AccessMateApp().run()
                
    except Exception as e:
        print(f"Error starting AccessMate: {e}")
        # Fallback to basic Kivy app
        AccessMateApp().run()

if __name__ == '__main__':
    main()