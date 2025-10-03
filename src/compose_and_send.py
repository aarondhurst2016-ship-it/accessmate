"""
compose_and_send.py - Compose, edit, review, and send text to Word, Notepad, or any word-based program.
- Supports step-by-step message building, editing, reading aloud, and sending via automation.
- Windows only (uses pywinauto for automation).
"""

import pyttsx3
import sys
import time
import subprocess
if sys.platform.startswith('win'):
    import pywinauto

engine = pyttsx3.init()

class MessageComposer:
    def __init__(self):
        self.lines = []

    def add_line(self, text):
        self.lines.append(text)

    def delete_last(self):
        if self.lines:
            self.lines.pop()

    def clear(self):
        self.lines = []

    def get_message(self):
        return '\n'.join(self.lines)

    def read_aloud(self):
        msg = self.get_message()
        if msg:
            engine.say(msg)
            engine.runAndWait()
        else:
            engine.say("No message to read.")
            engine.runAndWait()


    def send_to_app(self, app_name="Notepad", save_after=False):
        msg = self.get_message()
        if not msg:
            engine.say("No message to send.")
            engine.runAndWait()
            return False
        try:
            if sys.platform.startswith('win'):
                app = pywinauto.Application(backend="uia").connect(title_re=f".*{app_name}.*", found_index=0)
                win = app.top_window()
                win.set_focus()
                time.sleep(0.5)
                win.type_keys(msg, with_spaces=True, pause=0.01)
                engine.say(f"Message sent to {app_name}.")
                engine.runAndWait()
                if save_after:
                    win.type_keys('^s', pause=0.01)
                    engine.say(f"Save command sent to {app_name}.")
                    engine.runAndWait()
                return True
            elif sys.platform == 'darwin':
                # macOS: Use AppleScript to type and save in TextEdit or Word
                # Fix f-string with backslash issue
                escaped_msg = msg.replace('"', '\\"')
                save_command = 'keystroke "s" using command down' if save_after else ''
                script = f'''
                tell application "{app_name}"
                    activate
                    delay 0.5
                    tell application "System Events"
                        keystroke "{escaped_msg}"
                        {save_command}
                    end tell
                end tell
                '''
                subprocess.run(["osascript", "-e", script], check=True)
                engine.say(f"Message sent to {app_name}.")
                engine.runAndWait()
                return True
            elif sys.platform.startswith('linux'):
                # Linux: Use xdotool to type and save in gedit, LibreOffice, etc.
                # User must focus the editor window manually before running this.
                subprocess.run(["xdotool", "type", msg])
                engine.say(f"Message sent to {app_name} (focus window first).",)
                engine.runAndWait()
                if save_after:
                    subprocess.run(["xdotool", "key", "ctrl+s"])
                    engine.say(f"Save command sent to {app_name}.")
                    engine.runAndWait()
                return True
            else:
                engine.say("Platform not supported for automation.")
                engine.runAndWait()
                return False
        except Exception as e:
            engine.say(f"Could not send message to {app_name}: {e}")
            engine.runAndWait()
            return False

if __name__ == "__main__":
    composer = MessageComposer()
    print("Compose your message. Type commands: add <text>, delete, clear, read, send <app>, quit")
    while True:
        cmd = input("> ").strip()
        if cmd.lower() == "quit":
            break
        elif cmd.startswith("add "):
            composer.add_line(cmd[4:])
        elif cmd == "delete":
            composer.delete_last()
        elif cmd == "clear":
            composer.clear()
        elif cmd == "read":
            composer.read_aloud()
        elif cmd.startswith("send"):
            parts = cmd.split()
            app = parts[1] if len(parts) > 1 else "Notepad"
            save = (len(parts) > 2 and parts[2].lower() == "save")
            composer.send_to_app(app, save_after=save)
        elif cmd == "show":
            print(composer.get_message())
        else:
            print("Commands: add <text>, delete, clear, read, send <app> [save], show, quit")
