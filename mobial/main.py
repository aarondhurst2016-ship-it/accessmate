
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from gui import TalkbackGUI
from auto_update import auto_update_main

class TalkbackApp(App):
    def build(self):
        return TalkbackGUI()

import threading

if __name__ == "__main__":
    CURRENT_VERSION = "1.0.0"
    UPDATE_URL = "https://your-server.com/talkback/update.json"
    threading.Thread(target=auto_update_main, args=(CURRENT_VERSION, UPDATE_URL), daemon=True).start()
    TalkbackApp().run()
