"""
OCR Screen Reader Module
Provides OCR-based screen reading for images and PDFs using pytesseract and gtts.
"""
import pytesseract
from PIL import Image
import os
import tempfile
import pygame

# Conditional import for gtts - handle cases where it's not available
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    print("[WARNING] gtts not available - TTS features may be limited")
    GTTS_AVAILABLE = False
    gTTS = None

import sys
import platform



# --- Ultra-low-power mode control (auto/on/off) ---
ULTRA_LOW_POWER_MODE = None  # None=auto, True=on, False=off

def detect_ultra_low_power_mode():
    """Auto-detect based on hardware and battery level."""
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        cpu_count = psutil.cpu_count(logical=False) or 1
        # Battery check (if available)
        battery = psutil.sensors_battery()
        low_battery = battery and battery.percent is not None and battery.percent < 20
        # Heuristic: <2GB RAM, <2 CPU cores, or low battery = ultra low power
        if ram_gb < 2 or cpu_count < 2 or low_battery:
            return True
        return False
    except Exception:
        return True

def set_ultra_low_power_mode(mode):
    """Set ultra-low-power mode: True=on, False=off, None=auto."""
    global ULTRA_LOW_POWER_MODE
    if mode is None:
        ULTRA_LOW_POWER_MODE = detect_ultra_low_power_mode()
    else:
        ULTRA_LOW_POWER_MODE = bool(mode)

# Initialize mode (auto by default)
set_ultra_low_power_mode(None)

def get_ultra_low_power_mode():
    return ULTRA_LOW_POWER_MODE

class OCRScreenReader:
    """
    OCR Screen Reader optimized for ultra-low-power, low-memory, and legacy devices.
    Best practices:
    - Set ULTRA_LOW_POWER_MODE = True to aggressively minimize resource use.
    - Only activate camera or microphone when needed, release immediately after use.
    - Use lowest possible image resolution for OCR in ultra-low-power mode.
    - Use plain print() for TTS fallback if all else fails.
    - Avoid background polling or loops; use event-driven triggers.
    - Use lazy imports everywhere to reduce memory footprint.
    - Disable non-essential features (cloud, notifications, export, etc.) in ultra-low-power mode.
    - Supports Python 3.5+ (with reduced features for <3.7).
    - Platform/version checks and fallbacks for older OS/devices.
    """
    def sync_with_health_app(self, important_lines, target="google_fit"):
        """
        Stub for syncing extracted info with Apple Health or Google Fit.
        """
        # This is a stub. Real integration would require platform-specific APIs and user authentication.
        if target == "google_fit":
            self.tts("Syncing with Google Fit is not yet implemented. This requires OAuth and Google Fit API access.")
        elif target == "apple_health":
            self.tts("Syncing with Apple Health is not yet implemented. This requires HealthKit API access on iOS/macOS.")
        else:
            self.tts(f"Unknown health app target: {target}")
    def send_notification(self, title, message):
        """
        Send a real-time notification (Windows Toast). Requires win10toast.
        """
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=10)
            self.tts(f"Notification sent: {title} - {message}")
        except Exception as e:
            self.tts(f"Notification failed: {e}")

    def alert_for_appointments_and_meds(self, important_lines):
        """
        Scan important lines for appointments/medications and send notifications.
        """
        for line in important_lines:
            l = line.lower()
            if any(word in l for word in ["appointment", "consultation", "follow-up", "checkup", "date", "time"]):
                self.send_notification("Upcoming Appointment", line)
            if any(word in l for word in ["medication", "prescription", "pharmacy", "treatment", "dose", "tablet", "pill", "mg", "ml"]):
                self.send_notification("Medication Reminder", line)
    def generate_accessibility_report(self, important_lines, filename="accessibility_report.txt"):
        """
        Generate a summary report of detected appointments, contacts, and medications.
        """
        appointments = []
        contacts = []
        medications = []
        for line in important_lines:
            l = line.lower()
            if any(word in l for word in ["appointment", "consultation", "follow-up", "checkup", "date", "time"]):
                appointments.append(line)
            if any(word in l for word in ["phone", "contact", "address", "room", "clinic", "hospital"]):
                contacts.append(line)
            if any(word in l for word in ["medication", "prescription", "pharmacy", "treatment", "dose", "tablet", "pill", "mg", "ml"]):
                medications.append(line)
        report = ["Accessibility Report:"]
        report.append("\nAppointments:")
        report.extend(appointments if appointments else ["None found."])
        report.append("\nContacts:")
        report.extend(contacts if contacts else ["None found."])
        report.append("\nMedications:")
        report.extend(medications if medications else ["None found."])
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))
        self.tts(f"Accessibility report generated: {filename}")
        return filename
    def export_as_pdf(self, important_lines, filename="important_info.pdf"):
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in important_lines:
                pdf.cell(200, 10, txt=line, ln=1, align='L')
            pdf.output(filename)
            self.tts(f"Exported important info as PDF: {filename}")
        except Exception as e:
            self.tts(f"PDF export failed: {e}")

    def export_as_word(self, important_lines, filename="important_info.docx"):
        try:
            from docx import Document
            doc = Document()
            for line in important_lines:
                doc.add_paragraph(line)
            doc.save(filename)
            self.tts(f"Exported important info as Word document: {filename}")
        except Exception as e:
            self.tts(f"Word export failed: {e}")

    def export_as_ics(self, event_lines, filename="important_event.ics"):
        try:
            from ics import Calendar, Event
            c = Calendar()
            for line in event_lines:
                e = Event()
                e.name = line[:60]
                c.events.add(e)
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(c)
            self.tts(f"Exported events as ICS calendar file: {filename}")
        except Exception as e:
            self.tts(f"ICS export failed: {e}")

    def export_as_vcard(self, contact_lines, filename="important_contact.vcf"):
        try:
            vcard = "BEGIN:VCARD\nVERSION:3.0\n"
            for line in contact_lines:
                vcard += f"NOTE:{line}\n"
            vcard += "END:VCARD\n"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(vcard)
            self.tts(f"Exported contacts as vCard: {filename}")
        except Exception as e:
            self.tts(f"vCard export failed: {e}")
    def backup_to_google_drive(self, filename="important_info.txt"):
        """
        Upload the important info file to Google Drive using pydrive2.
        """
        try:
            from pydrive2.auth import GoogleAuth
            from pydrive2.drive import GoogleDrive
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            file1 = drive.CreateFile({'title': filename})
            file1.SetContentFile(filename)
            file1.Upload()
            self.tts(f"Backed up {filename} to Google Drive.")
        except Exception as e:
            self.tts(f"Google Drive backup failed: {e}")
    def smart_search(self, document_text, query):
        """
        Basic smart search: find lines in document_text that match query keywords.
        """
        q = query.lower().strip()
        results = []
        for line in document_text.splitlines():
            if q in line.lower():
                results.append(line)
        if results:
            self.tts(f"Found {len(results)} result(s) for '{query}':")
            for r in results:
                self.tts(r)
        else:
            self.tts(f"No results found for '{query}'.")
        return results
    def record_and_transcribe_audio(self, duration=10):
        """
        Record audio from the microphone and transcribe it to text.
        """
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            self.tts(f"Recording for {duration} seconds. Please speak now.")
            with mic as source:
                audio = recognizer.listen(source, timeout=duration)
            self.tts("Transcribing audio...")
            text = recognizer.recognize_google(audio)
            self.tts("Transcription complete.")
            important, rest = self.extract_important_info(text)
            if important:
                self.tts("Important spoken information:")
                for line in important:
                    self.tts(line)
            if rest:
                self.tts("Other spoken details:")
                self.tts("\n".join(rest))
            return text
        except Exception as e:
            self.tts(f"Error recording/transcribing audio: {e}")
            return None
    def read_handwriting(self, image_path):
        """
        Use Tesseract configs to improve recognition of handwritten notes.
        """
        try:
            custom_config = r'--oem 1 --psm 1'
            text = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
            important, rest = self.extract_important_info(text)
            if important:
                self.tts("Important handwritten information:")
                for line in important:
                    self.tts(line)
            if rest:
                self.tts("Other handwritten details:")
                self.tts("\n".join(rest))
            return text
        except Exception as e:
            self.tts(f"Error reading handwriting: {e}")
            return None
    def get_vault_key(self, password):
        try:
            from cryptography.fernet import Fernet
            import base64
            import hashlib
            # Derive a Fernet key from the password
            key = hashlib.sha256(password.encode()).digest()
            return base64.urlsafe_b64encode(key)
        except Exception:
            return None

    def save_encrypted_info(self, important_lines, password, filename="vault.enc"):
        try:
            from cryptography.fernet import Fernet
            key = self.get_vault_key(password)
            if not key:
                self.tts("Encryption unavailable. Please install cryptography.")
                return
            f = Fernet(key)
            text = '\n'.join(important_lines).encode()
            token = f.encrypt(text)
            with open(filename, 'wb') as file:
                file.write(token)
            self.tts(f"Encrypted info saved to {filename}.")
        except Exception:
            self.tts("Failed to encrypt and save info.")

    def load_encrypted_info(self, password, filename="vault.enc"):
        try:
            from cryptography.fernet import Fernet
            key = self.get_vault_key(password)
            if not key:
                self.tts("Decryption unavailable. Please install cryptography.")
                return None
            f = Fernet(key)
            with open(filename, 'rb') as file:
                token = file.read()
            text = f.decrypt(token).decode()
            self.tts("Decrypted info:")
            self.tts(text)
            return text
        except Exception:
            self.tts("Failed to decrypt info. Wrong password or corrupted file.")
            return None
    def listen_for_ocr_commands(self, last_text=None):
        """
        Listen for voice commands to control OCR actions (repeat, save, stop, etc.).
        """
        try:
            import speech_recognition as sr
        except ImportError:
            self.tts("speech_recognition not installed. Voice commands unavailable.")
            return
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        self.tts("Say a command: repeat, save, stop, or next.")
        while True:
            with mic as source:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    cmd = recognizer.recognize_google(audio).strip().lower()
                except Exception:
                    continue
            if cmd == "repeat":
                if last_text:
                    self.tts(last_text)
                else:
                    self.tts("Nothing to repeat.")
            elif cmd == "save":
                if last_text:
                    self.save_important_info([last_text], filename="important_info.txt", copy_clipboard=True)
                else:
                    self.tts("Nothing to save.")
            elif cmd == "stop":
                self.tts("Stopping voice command control.")
                break
            elif cmd == "next":
                self.tts("Next action not implemented.")
            else:
                self.tts(f"Unknown command: {cmd}")
    def summarize_text(self, text, sentence_count=3):
        try:
            from sumy.parsers.plaintext import PlaintextParser
            from sumy.nlp.tokenizers import Tokenizer
            from sumy.summarizers.text_rank import TextRankSummarizer
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = TextRankSummarizer()
            summary = summarizer(parser.document, sentence_count)
            return " ".join(str(sentence) for sentence in summary)
        except Exception:
            return None
    def detect_language(self, text):
        try:
            from langdetect import detect
            lang = detect(text)
            return lang
        except Exception:
            return None

    def offer_translation(self, text, target_lang='en'):
        try:
            from googletrans import Translator
            lang = self.detect_language(text)
            if not lang or lang == target_lang:
                return
            self.tts(f"Document language detected: {lang}. Would you like a translation to {target_lang}?")
            translator = Translator()
            translated = translator.translate(text, src=lang, dest=target_lang)
            self.tts("Here is the translated important information:")
            self.tts(translated.text)
        except ImportError:
            print("[WARNING] googletrans not available - translation features disabled")
            self.tts("Translation features are not available in this version.")
        except Exception as e:
            print(f"[WARNING] Translation failed: {e}")
            self.tts("Translation unavailable due to an error.")
    def save_important_info(self, important_lines, filename=None, copy_clipboard=True):
        """
        Save important lines to a file and/or copy to clipboard.
        """
        if not important_lines:
            return
        text = '\n'.join(important_lines)
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            self.tts(f"Important information saved to {filename}.")
        if copy_clipboard:
            try:
                import pyperclip
                pyperclip.copy(text)
                self.tts("Important information copied to clipboard.")
            except ImportError:
                self.tts("pyperclip not installed. Clipboard copy unavailable.")
    def extract_contacts_locations(self, text):
        """
        Extracts phone numbers and addresses from text. Returns lists of (type, value, context_line).
        """
        phone_pattern = r'(\+?\d[\d\-\s]{7,}\d)'
        # Simple address pattern: lines with numbers and street/road/ave/etc.
        address_keywords = ['street', 'st.', 'road', 'rd.', 'avenue', 'ave', 'blvd', 'lane', 'ln.', 'drive', 'dr.', 'court', 'ct.', 'circle', 'cir.', 'way', 'suite', 'apt', 'building', 'floor', 'hospital', 'clinic']
        found = []
        for line in text.splitlines():
            # Phone numbers
            for m in self.re.findall(phone_pattern, line):
                found.append(('phone', m, line))
            # Addresses
            l = line.lower()
            if any(k in l for k in address_keywords) and any(char.isdigit() for char in line):
                found.append(('address', line.strip(), line))
        return found

    def offer_contact_location_actions(self, found_contacts):
        """
        Offer to call, map, or save found phone numbers/addresses (prints for now, can integrate with phone/map APIs).
        """
        if not found_contacts:
            return
        self.tts("I found the following contact information. Would you like to call, map, or save them?")
        for typ, val, context in found_contacts:
            if typ == 'phone':
                self.tts(f"Phone number: {val} in: {context}")
            elif typ == 'address':
                self.tts(f"Address: {val}")
        print("[Contact/Location] To act on: ", found_contacts)
    import re
    from datetime import datetime, timedelta

    def extract_dates_times(self, text):
        """
        Extracts date and time strings from text. Returns a list of (date/time, context_line).
        """
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # 12/31/2025
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # 12-31-2025
            r'\b\d{1,2} [A-Za-z]+ \d{2,4}\b', # 31 December 2025
            r'\b[A-Za-z]+ \d{1,2},? \d{2,4}\b', # December 31, 2025
        ]
        time_patterns = [
            r'\b\d{1,2}:\d{2}(?: ?[APMapm]{2})?\b', # 14:30, 2:30 PM
            r'\b\d{1,2} ?[APMapm]{2}\b', # 2 PM
        ]
        found = []
        for line in text.splitlines():
            for pat in date_patterns:
                for m in self.re.findall(pat, line):
                    found.append((m, line))
            for pat in time_patterns:
                for m in self.re.findall(pat, line):
                    found.append((m, line))
        return found

    def offer_reminder(self, found_dates_times):
        """
        Offer to add reminders for found dates/times (prints for now, can integrate with calendar/reminder system).
        """
        if not found_dates_times:
            return
        self.tts("I found the following dates and times. Would you like to add a reminder?")
        for dt, context in found_dates_times:
            self.tts(f"{dt} in: {context}")
        # Placeholder: In a GUI, prompt user to confirm adding reminder.
        # Here, just print to console.
        print("[Reminder] To add: ", found_dates_times)
    DEFAULT_KEYWORDS = [
        'doctor', 'dr.', 'appointment', 'date', 'time', 'location', 'address', 'clinic', 'hospital', 'prescription', 'medication', 'phone', 'contact', 'room', 'patient', 'specialist', 'consultation', 'follow-up', 'referral', 'test', 'scan', 'lab', 'results', 'procedure', 'treatment', 'surgery', 'checkup', 'gp', 'practice', 'nurse', 'pharmacy', 'urgent', 'emergency', 'note', 'important', 'reminder', 'cancel', 'reschedule', 'confirm', 'arrive', 'bring', 'insurance', 'id', 'number', 'dob', 'birth', 'time:'
    ]

    def load_keywords(self):
        try:
            import json
            if os.path.exists('user_keywords.json'):
                with open('user_keywords.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return self.DEFAULT_KEYWORDS.copy()

    def save_keywords(self, keywords):
        try:
            import json
            with open('user_keywords.json', 'w', encoding='utf-8') as f:
                json.dump(keywords, f)
        except Exception:
            pass

    def add_keyword(self, keyword):
        keywords = self.load_keywords()
        if keyword.lower() not in [k.lower() for k in keywords]:
            keywords.append(keyword)
            self.save_keywords(keywords)
            self.tts(f"Keyword '{keyword}' added.")
        else:
            self.tts(f"Keyword '{keyword}' already exists.")

    def remove_keyword(self, keyword):
        keywords = self.load_keywords()
        keywords = [k for k in keywords if k.lower() != keyword.lower()]
        self.save_keywords(keywords)
        self.tts(f"Keyword '{keyword}' removed.")

    def extract_important_info(self, text):
        """
        Extracts and highlights important lines containing keywords (user-customizable).
        Returns (important_lines, rest_of_text)
        """
        keywords = self.load_keywords()
        lines = text.splitlines()
        important = []
        rest = []
        for line in lines:
            l = line.lower()
            if any(k.lower() in l for k in keywords):
                important.append(line)
            else:
                rest.append(line)
        return important, rest
    def __init__(self, tts_func=None):
        self.tts = tts_func or self.default_tts
        self.is_legacy_python = sys.version_info < (3,7)
        self.platform = platform.system().lower()
        self.ultra_low_power = ULTRA_LOW_POWER_MODE
        if not self.ultra_low_power:
            try:
                if pygame:
                    pygame.mixer.init()
            except Exception:
                pass

    def default_tts(self, text):
        # Ultra-low-power: always use print as fallback
        if self.ultra_low_power:
            print("[TTS ultra-low-power] {}".format(text))
            return
        
        # Check if gTTS is available
        if not GTTS_AVAILABLE:
            print("[TTS fallback - gTTS not available] {}".format(text))
            return
            
        try:
            import tempfile
            if 'pygame' in globals() and pygame:
                import pygame
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts.save(fp.name)
                try:
                    if 'pygame' in globals() and pygame:
                        pygame.mixer.music.load(fp.name)
                        pygame.mixer.music.play()
                    else:
                        print("[TTS] {}".format(text))
                finally:
                    os.remove(fp.name)
        except Exception:
            print("[TTS fallback] {}".format(text))

    def read_image(self, image_path, low_res=True):
        """
        Read and OCR an image, optimized for ultra-low-end and legacy devices.
        If low_res is True, downscale image before OCR to save memory/CPU.
        In ultra-low-power mode, aggressively downscale and skip non-essential features.
        """
        try:
            from PIL import Image
            import pytesseract
            img = Image.open(image_path)
            if self.ultra_low_power:
                img.thumbnail((640, 640))  # Aggressive downscale
            elif low_res:
                img.thumbnail((1024, 1024))
            if self.is_legacy_python:
                text = pytesseract.image_to_string(img, lang='eng')
            else:
                text = pytesseract.image_to_string(img)
            important, rest = self.extract_important_info(text)
            if not self.ultra_low_power:
                found_dates_times = self.extract_dates_times(text)
                self.offer_reminder(found_dates_times)
                found_contacts = self.extract_contacts_locations(text)
                self.offer_contact_location_actions(found_contacts)
            last_spoken = None
            if important:
                self.tts("Important information:")
                for line in important:
                    self.tts(line)
                    last_spoken = line
                if not self.ultra_low_power:
                    self.save_important_info(important, filename="important_info.txt", copy_clipboard=True)
                    self.offer_translation("\n".join(important), target_lang='en')
                    summary = self.summarize_text("\n".join(important))
                    if summary:
                        self.tts("Summary of important information:")
                        self.tts(summary)
            if rest:
                self.tts("Other details:")
                self.tts("\n".join(rest))
            if not self.ultra_low_power:
                self.listen_for_ocr_commands(last_text=last_spoken)
            return text
        except Exception as e:
            self.tts("Error reading image: {}".format(e))
            return None

    def read_pdf(self, pdf_path):
        try:
            from pdf2image import convert_from_path
        except ImportError:
            self.tts("pdf2image not installed. Cannot read PDFs.")
            return None
        try:
            pages = convert_from_path(pdf_path)
            full_text = ""
            for page in pages:
                text = pytesseract.image_to_string(page)
                full_text += text + "\n"
            important, rest = self.extract_important_info(full_text)
            found_dates_times = self.extract_dates_times(full_text)
            self.offer_reminder(found_dates_times)
            found_contacts = self.extract_contacts_locations(full_text)
            self.offer_contact_location_actions(found_contacts)
            last_spoken = None
            if important:
                self.tts("Important information:")
                for line in important:
                    self.tts(line)
                    last_spoken = line
                # Save/export important info
                self.save_important_info(important, filename="important_info.txt", copy_clipboard=True)
                # Language detection and translation
                self.offer_translation("\n".join(important), target_lang='en')
                # Summarize important info
                summary = self.summarize_text("\n".join(important))
                if summary:
                    self.tts("Summary of important information:")
                    self.tts(summary)
            if rest:
                self.tts("Other details:")
                self.tts("\n".join(rest))
            # Start voice command control
            self.listen_for_ocr_commands(last_text=last_spoken)
            return full_text
        except Exception as e:
            self.tts(f"Error reading PDF: {e}")
            return None

# Example usage:

def cli_toggle():
    print("Ultra-low-power mode is currently:", get_ultra_low_power_mode())
    print("Type 'on', 'off', or 'auto' to change mode, or 'q' to quit.")
    while True:
        cmd = input("Mode> ").strip().lower()
        if cmd == 'on':
            set_ultra_low_power_mode(True)
        elif cmd == 'off':
            set_ultra_low_power_mode(False)
        elif cmd == 'auto':
            set_ultra_low_power_mode(None)
        elif cmd == 'q':
            break
        print("Ultra-low-power mode is now:", get_ultra_low_power_mode())

def tk_toggle():
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Ultra Low Power Mode Toggle")
        status = tk.StringVar()
        def update_status():
            status.set(f"Current: {get_ultra_low_power_mode()}")
        def set_on():
            set_ultra_low_power_mode(True)
            update_status()
        def set_off():
            set_ultra_low_power_mode(False)
            update_status()
        def set_auto():
            set_ultra_low_power_mode(None)
            update_status()
        tk.Label(root, text="Ultra Low Power Mode").pack()
        tk.Label(root, textvariable=status).pack()
        tk.Button(root, text="On", command=set_on).pack()
        tk.Button(root, text="Off", command=set_off).pack()
        tk.Button(root, text="Auto", command=set_auto).pack()
        update_status()
        root.mainloop()
    except Exception as e:
        print(f"Tkinter UI unavailable: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        tk_toggle()
    else:
        cli_toggle()
