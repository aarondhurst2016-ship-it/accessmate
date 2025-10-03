# Cross-platform GUI for Talkback Assistant using Kivy

# Kivy-based cross-platform GUI for Talkback Assistant
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# Import feature modules
import speech
from speech import say_time, say_date, say_weather, list_microphones
import reminders, notes, calendar_integration, email_integration, smart_home, file_manager, media, location, translation, health, security, dashboard
from help_sheet import HELP_TEXT

def enable_accessibility(widget, tooltip=None):
    # TODO: Implement Kivy accessibility features (tooltips, speech feedback)
    pass

class TalkbackGUI(BoxLayout):
    def run_auto_update(self, instance):
        from auto_update import auto_update_main
        # You may want to set these dynamically or from settings
        current_version = "1.0.0"
        update_url = "https://your-update-server.com/update.json"
        auto_update_main(current_version, update_url)
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(title='Auto-Update', content=Label(text='Update check complete. See console for details.'), size_hint=(0.7, 0.3))
        popup.open()
    def show_setup_instructions(self, instance):
        import platform, os
        instructions = ""
        sys_platform = platform.system()
        if sys_platform == "Windows":
            path = os.path.join(os.path.dirname(__file__), '../windows_startup_instructions.txt')
        elif sys_platform == "Darwin":
            path = os.path.join(os.path.dirname(__file__), '../macos_startup_instructions.txt')
        elif sys_platform == "Linux":
            path = os.path.join(os.path.dirname(__file__), '../linux_startup_instructions.txt')
        else:
            path = None
        if path and os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                instructions = f.read()
        else:
            instructions = "Refer to the README for platform-specific auto-start setup."
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        text = TextInput(text=instructions + "\n\nFollow these steps to enable auto-start for your platform.", readonly=True, font_size=16, size_hint_y=0.8)
        box.add_widget(text)
        def copy_to_clipboard(instance):
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text.text)
        copy_btn = Button(text='Copy Instructions', size_hint_y=0.2)
        copy_btn.bind(on_press=copy_to_clipboard)
        box.add_widget(copy_btn)
        popup = Popup(title='Auto-Start Setup', content=box, size_hint=(0.9, 0.7))
        popup.open()
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = 20
        self.spacing = 10

        # Automatically check for updates at startup
        from auto_update import auto_update_main, check_for_app_update
        current_version = "1.0.0"
        update_url = "https://your-update-server.com/update.json"
        new_url = check_for_app_update(current_version, update_url)
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        if new_url:
            msg = "A new version is available and will be downloaded now."
            from auto_update import apply_update
            apply_update(new_url)
        else:
            msg = "Your app is up to date."
        popup = Popup(title='Update Status', content=Label(text=msg), size_hint=(0.7, 0.3))
        popup.open()

        # Setup button for auto-start configuration
        setup_btn = Button(text='Setup Auto-Start', size_hint=(1, None), height=50)
        setup_btn.bind(on_press=self.show_setup_instructions)
        enable_accessibility(setup_btn, tooltip='Configure app to start automatically on your device.')
        self.add_widget(setup_btn)

        # Auto-Update button
        update_btn = Button(text='Check for Updates', size_hint=(1, None), height=50)
        update_btn.bind(on_press=self.run_auto_update)
        enable_accessibility(update_btn, tooltip='Check for new app updates and install automatically.')
        self.add_widget(update_btn)

        self.add_widget(Label(text='Welcome to Talkback Assistant!', font_size=24, size_hint=(1, None), height=40))

        # Microphone selection
        mic_names = list_microphones()
        self.mic_spinner = Spinner(
            text=mic_names[0] if mic_names else 'Select Microphone',
            values=mic_names,
            size_hint=(1, None),
            height=44
        )
        self.mic_spinner.bind(text=self.set_mic)
        self.add_widget(self.mic_spinner)
        enable_accessibility(self.mic_spinner, tooltip='Choose which microphone to use for speech input.')

        # Scrollable feature grid
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Feature buttons and their actions
        features = [
            ('Screen Reader ON/OFF', self.screen_reader),
            ('Settings', self.settings),
            ('Help', self.show_help),
            ('Say Time', lambda i: say_time()),
            ('Say Date', lambda i: say_date()),
            ('Say Weather', lambda i: say_weather()),
            ('Reminders & Alarms', self.reminders),
            ('Calendar', self.calendar),
            ('Notes & To-Do', self.notes),
            ('Email', self.email),
            ('Smart Home', self.smart_home),
            ('File Manager', self.file_manager),
            ('Media', self.media),
            ('Location', self.location),
            ('Translation', self.translation),
            ('Health', self.health),
            ('Security', self.security),
            ('Dashboard', self.dashboard),
        ]
        for label, action in features:
            btn = Button(text=label, size_hint_y=None, height=50)
            btn.bind(on_press=action)
            enable_accessibility(btn, tooltip=label)
            grid.add_widget(btn)

        scroll.add_widget(grid)
        self.add_widget(scroll)

    def set_mic(self, spinner, text):
        mic_names = list_microphones()
        idx = mic_names.index(text) if text in mic_names else None
        speech.selected_mic_index = idx

    def screen_reader(self, instance):
        # TODO: Implement screen reader toggle
        pass

    def settings(self, instance):
        # TODO: Implement settings dialog
        pass

    def show_help(self, instance):
        # Show help sheet
        from speech import speak
        speak(HELP_TEXT)

    def reminders(self, instance):
        # TODO: Integrate reminders
        pass

    def calendar(self, instance):
        # TODO: Integrate calendar
        pass

    def notes(self, instance):
        # TODO: Integrate notes
        pass

    def email(self, instance):
        # TODO: Integrate email
        pass

    def smart_home(self, instance):
        # TODO: Integrate smart home
        pass

    def file_manager(self, instance):
        # TODO: Integrate file manager
        pass

    def media(self, instance):
        # TODO: Integrate media
        pass

    def location(self, instance):
        # TODO: Integrate location
        pass

    def translation(self, instance):
        # TODO: Integrate translation
        pass

    def health(self, instance):
        # TODO: Integrate health
        pass

    def security(self, instance):
        # TODO: Integrate security
        pass

    def dashboard(self, instance):
        # TODO: Integrate dashboard
        pass

class TalkbackApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.13, 0.13, 0.13, 1)
        try:
            Window.set_icon('logo.svg')
        except Exception:
            pass
        # Optionally, show logo as splash
        from kivy.uix.image import Image
        from kivy.uix.boxlayout import BoxLayout
        splash = BoxLayout(orientation='vertical')
        splash.add_widget(Image(source='logo.svg', size_hint=(1, 0.3)))
        gui = TalkbackGUI()
        splash.add_widget(gui)
        return splash

if __name__ == '__main__':
    TalkbackApp().run()
