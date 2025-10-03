# voice_commands.py
# Central voice command handler for all features



import threading
import time
import pyttsx3
import speech_recognition as sr

# Mobile background service support
try:
    from plyer import notification
    from plyer import vibrator
    from plyer import audio
    from plyer import tts
    mobile_background = True
except ImportError:
    mobile_background = False

engine = pyttsx3.init()
from email_integration import read_emails

# Automatically start email announcement thread on module load
def _auto_start_email_announcement():
    try:
        start_email_announcement_thread()
        print("Email announcement thread started automatically.")
    except Exception as e:
        print(f"Failed to start email announcement thread: {e}")

_auto_start_email_announcement()

# Automatically announce dangerous weather alerts for user's location
def announce_weather_alerts_loop(check_interval=600):
    from weather_alerts import get_weather_alerts
    from location import get_location
    announced = set()
    while True:
        try:
            city = get_location()
            alerts = get_weather_alerts(city)
            for alert in alerts:
                # Simple danger keyword check
                if any(word in alert.lower() for word in ["danger", "warning", "severe", "alert", "emergency"]):
                    if alert not in announced:
                        engine.say(f"Weather alert for your location: {alert}")
                        engine.runAndWait()
                        announced.add(alert)
        except Exception as e:
            print(f"Weather alert error: {e}")
        time.sleep(check_interval)

def start_weather_alert_announcement_thread():
    t = threading.Thread(target=announce_weather_alerts_loop, daemon=True)
    t.start()

start_weather_alert_announcement_thread()
def announce_new_emails_loop(provider, username, password, check_interval=60):
    last_seen_ids = set()
    while True:
        try:
            emails = read_emails(provider, username, password, unread_only=True, num=5)
            new_ids = set()
            for mail in emails:
                # Use subject+from as a simple unique id
                mail_id = f"{mail['from']}|{mail['subject']}"
                new_ids.add(mail_id)
                if mail_id not in last_seen_ids:
                    engine.say(f"New email from {mail['from']}. Subject: {mail['subject']}.")
            if new_ids - last_seen_ids:
                engine.runAndWait()
            last_seen_ids = new_ids
        except Exception as e:
            print(f"Error announcing new emails: {e}")
        time.sleep(check_interval)

def start_email_announcement_thread():
    provider = "gmail"  # Default, can be changed or parsed from settings
    username = "your_email@gmail.com"  # Replace with your email
    password = "your_password"  # Replace with your password or use secure method
    t = threading.Thread(target=announce_new_emails_loop, args=(provider, username, password), daemon=True)
    t.start()


# Import feature functions here
from screen_reader import read_screen
from weather import get_weather
from notes import create_note
from remote_control import remote_action
from jokes import tell_joke
from fitness_tracker import log_workout, get_fitness_stats
from calendar_integration import sync_user_calendar, list_user_events
from medication_reminder import remind_medication
from emergency_contacts import add_emergency_contact, get_emergency_contacts
from expense_tracker import log_expense, get_expense_summary
from file_manager import search_files, open_file
from camera import capture_and_read_text, recognize_faces_from_camera
from document_scanner import scan_document
from dashboard import get_dashboard_widgets, set_dashboard_widget, get_map_directions_by_speech
from custom_shortcuts import create_shortcut, list_shortcuts
from contacts import get_contact_info
from call_integration import call_phone_twilio, open_whatsapp, open_messenger, open_phone_dialer
from language_learning import daily_vocabulary, quiz
from location import get_location, get_directions
from media import play_media

def handle_voice_command(command):
    if "live translate" in command or "live translation" in command:
        try:
            # On mobile, use plyer notification or tts
            if mobile_background:
                tts.speak("Live translation started.")
            else:
                import tkinter.simpledialog
            from speech import listen_and_translate, speak
            src_lang = tkinter.simpledialog.askstring("Live Translation", "Enter your language code (e.g. en):")
            tgt_lang = tkinter.simpledialog.askstring("Live Translation", "Enter partner's language code (e.g. es):")
            if not src_lang or not tgt_lang:
                engine.say("Language codes required.")
                engine.runAndWait()
                return
            engine.say(f"Live translation started: {src_lang} <-> {tgt_lang}. Say 'stop' to end.")
            engine.runAndWait()
            while True:
                engine.say(f"Speak in {src_lang}.")
                engine.runAndWait()
                text1 = listen_and_translate(src_lang, tgt_lang)
                if text1 and text1.strip().lower() == "stop":
                    break
                speak(text1, lang=tgt_lang)
                engine.say(f"Partner, speak in {tgt_lang}.")
                engine.runAndWait()
                text2 = listen_and_translate(tgt_lang, src_lang)
                if text2 and text2.strip().lower() == "stop":
                    break
                speak(text2, lang=src_lang)
            engine.say("Live translation ended.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Live translation error: {e}")
            engine.runAndWait()
    elif "weather alert" in command or "weather alerts" in command:
        try:
            from weather_alerts import get_weather_alerts
            city = "London"
            import re
            city_match = re.search(r'weather alerts? (.+)', command)
            if city_match:
                city = city_match.group(1)
            alerts = get_weather_alerts(city)
            if alerts:
                for alert in alerts:
                    engine.say(f"Weather alert: {alert}")
            else:
                engine.say("No weather alerts found.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error fetching weather alerts: {e}")
            engine.runAndWait()
    if "emergency need help" in command:
        try:
            contacts = get_emergency_contacts()
            from location import get_location
            location = get_location()
            # Call up to 5 contacts and send location via WhatsApp
            for contact in contacts[:5]:
                number = contact.get('number')
                if number:
                    engine.say(f"Contacting emergency contact {contact.get('name','')} at {number} and sending location via WhatsApp.")
                    engine.runAndWait()
                    open_phone_dialer(number)
                    # Send location via WhatsApp
                    from call_integration import open_whatsapp
                    message = f"Emergency! I need help. My location: {location}"
                    open_whatsapp(number, message)
            if not contacts:
                engine.say("No emergency contacts found.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error contacting emergency contacts: {e}")
            engine.runAndWait()
    if "create meeting invite" in command or "send meeting invite" in command:
        try:
            from calendar_integration import create_meeting_invite
            import re
            title_match = re.search(r'title ([^ ]+)', command)
            start_match = re.search(r'start ([^ ]+)', command)
            end_match = re.search(r'end ([^ ]+)', command)
            attendees_match = re.search(r'attendees ([^ ]+)', command)
            location_match = re.search(r'location ([^ ]+)', command)
            description_match = re.search(r'description ([^ ]+)', command)
            title = title_match.group(1) if title_match else "Meeting"
            start_time = start_match.group(1) if start_match else None
            end_time = end_match.group(1) if end_match else None
            attendees = attendees_match.group(1).split(',') if attendees_match else []
            location = location_match.group(1) if location_match else None
            description = description_match.group(1) if description_match else None
            invite = create_meeting_invite(title, start_time, end_time, attendees, location, description)
            engine.say(f"Meeting invite '{title}' created for {', '.join(attendees)}.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error creating meeting invite: {e}")
            engine.runAndWait()
    if "start email announcements" in command or "announce new emails" in command:
        start_email_announcement_thread()
        engine.say("New email announcements enabled.")
        engine.runAndWait()
    if "reply to email" in command:
        try:
            from email_integration import send_email, read_emails
            provider = "gmail"  # Default, can be changed or parsed from command
            username = "your_email@gmail.com"  # Replace with your email
            password = "your_password"  # Replace with your password or use secure method
            emails = read_emails(provider, username, password)
            if emails:
                last_email = emails[-1]
                reply_body = command.split("reply to email",1)[1].strip() or "Replying to your email."
                result = send_email(provider, username, password, last_email['from'], f"Re: {last_email['subject']}", reply_body)
                if result:
                    engine.say("Reply sent successfully.")
                else:
                    engine.say("Failed to send reply.")
                engine.runAndWait()
            else:
                engine.say("No emails to reply to.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error replying to email: {e}")
            engine.runAndWait()
    if "forward email" in command:
        try:
            from email_integration import send_email, read_emails
            import re
            # Simple contact lookup
            contacts = {
                "bob": "bob@example.com",
                "alice": "alice@example.com",
                "john": "john@example.com"
            }
            provider = "gmail"  # Default, can be changed or parsed from command
            username = "your_email@gmail.com"  # Replace with your email
            password = "your_password"  # Replace with your password or use secure method
            emails = read_emails(provider, username, password)
            if emails:
                last_email = emails[-1]
                to_addr_match = re.search(r'to ([^ ]+)', command)
                to_addr = to_addr_match.group(1) if to_addr_match else "recipient@example.com"
                # If not an email address, look up contact name
                if "@" not in to_addr:
                    to_addr = contacts.get(to_addr.lower(), "recipient@example.com")
                result = send_email(provider, username, password, to_addr, f"Fwd: {last_email['subject']}", last_email['body'])
                if result:
                    engine.say(f"Email forwarded to {to_addr} successfully.")
                else:
                    engine.say("Failed to forward email.")
                engine.runAndWait()
            else:
                engine.say("No emails to forward.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error forwarding email: {e}")
            engine.runAndWait()
    if "send email" in command:
        try:
            from email_integration import send_email
            import re
            # Simple contact lookup
            contacts = {
                "bob": "bob@example.com",
                "alice": "alice@example.com",
                "john": "john@example.com"
            }
            provider = "gmail"  # Default, can be changed or parsed from command
            username = "your_email@gmail.com"  # Replace with your email
            password = "your_password"  # Replace with your password or use secure method
            to_addr_match = re.search(r'to ([^ ]+)', command)
            to_addr = to_addr_match.group(1) if to_addr_match else "recipient@example.com"
            # If not an email address, look up contact name
            if "@" not in to_addr:
                to_addr = contacts.get(to_addr.lower(), "recipient@example.com")
            subject = re.search(r'subject (.+?)(?: body|$)', command)
            body = re.search(r'body (.+)', command)
            subject = subject.group(1) if subject else "No Subject"
            body = body.group(1) if body else "No Body"
            # Attachments: parse file paths from command (e.g., 'attach file1.jpg,file2.pdf')
            attach_match = re.search(r'attach ([^ ]+)', command)
            attachments = None
            if attach_match:
                attachments = [f.strip() for f in attach_match.group(1).split(',')]
            result = send_email(provider, username, password, to_addr, subject, body, attachments=attachments)
            if result:
                engine.say(f"Email sent to {to_addr} successfully.")
            else:
                engine.say("Failed to send email.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error sending email: {e}")
            engine.runAndWait()
    if "read emails" in command or "read my emails" in command or "search emails" in command:
        try:
            from email_integration import read_emails
            import re
            provider = "gmail"  # Default, can be changed or parsed from command
            username = "your_email@gmail.com"  # Replace with your email
            password = "your_password"  # Replace with your password or use secure method
            unread_only = "unread" in command
            important_only = "important" in command or "urgent" in command
            # Parse search criteria
            sender_match = re.search(r'from ([^ ]+)', command)
            subject_match = re.search(r'subject ([^ ]+)', command)
            date_match = re.search(r'date ([^ ]+)', command)
            search_sender = sender_match.group(1) if sender_match else None
            search_subject = subject_match.group(1) if subject_match else None
            search_date = date_match.group(1) if date_match else None
            emails = read_emails(provider, username, password, unread_only=unread_only, important_only=important_only, search_sender=search_sender, search_subject=search_subject, search_date=search_date)
            if emails:
                for mail in emails:
                    engine.say(f"From: {mail['from']}. Subject: {mail['subject']}. Date: {mail.get('date','')}. Body: {mail['body']}")
                engine.runAndWait()
            else:
                engine.say("No emails found.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error reading emails: {e}")
            engine.runAndWait()
    if "who is in the room" in command or "recognize faces" in command or "who do you see" in command:
        try:
            from camera import recognize_faces_from_camera
            recognize_faces_from_camera()
        except Exception as e:
            engine.say(f"Error recognizing faces: {e}")
            engine.runAndWait()
    if "automate checkout" in command or "auto checkout" in command:
        try:
            from shopping_automation import automate_checkout
            import re
            url_match = re.search(r'(https?://\S+)', command)
            if url_match:
                url = url_match.group(1)
                result = automate_checkout(url)
                if result:
                    engine.say("Checkout automation started. Complete address and payment in browser.")
                else:
                    engine.say("Checkout automation failed.")
                engine.runAndWait()
            else:
                engine.say("No shop URL found in your command.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error automating checkout: {e}")
            engine.runAndWait()
    if "automate add to basket" in command or "auto add to basket" in command:
        try:
            from shopping_automation import automate_add_to_basket
            import re
            url_match = re.search(r'(https?://\S+)', command)
            if url_match:
                url = url_match.group(1)
                result = automate_add_to_basket(url)
                if result:
                    engine.say("Automated add to basket complete.")
                else:
                    engine.say("Automation failed.")
                engine.runAndWait()
            else:
                engine.say("No product URL found in your command.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error automating basket: {e}")
            engine.runAndWait()
    if "describe shopping item" in command or "shop item" in command:
        try:
            from shopping_accessibility import describe_online_item, add_to_basket
            import re
            url_match = re.search(r'(https?://\S+)', command)
            if url_match:
                url = url_match.group(1)
                item = describe_online_item(url)
                if item:
                    engine.say("Say 'add to basket' to add this item.")
                    engine.runAndWait()
            else:
                engine.say("No product URL found in your command.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error describing shopping item: {e}")
            engine.runAndWait()
    if "add to basket" in command:
        try:
            from shopping_accessibility import add_to_basket
            # This assumes the last described item URL is available; for demo, ask for URL
            import tkinter.simpledialog
            url = tkinter.simpledialog.askstring("Add to Basket", "Enter product URL:")
            if url:
                add_to_basket(url)
                engine.say("Item added to basket.")
                engine.runAndWait()
            else:
                engine.say("No URL entered.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error adding to basket: {e}")
            engine.runAndWait()
    if "get directions to" in command or "directions to" in command:
        try:
            from settings import Settings
            settings = Settings()
            settings.load("user_settings.json")
            mode = getattr(settings, "transport_mode", "foot")
            from location import get_directions
            destination = command.split("to",1)[1].strip()
            steps = get_directions(destination)
            for step in steps:
                engine.say(step)
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting directions: {e}")
            engine.runAndWait()
    if "shopping advice" in command or "should i buy this" in command:
        try:
            import cv2, pytesseract, json
            from PIL import Image
            from settings import Settings
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            item_name = None
            if ret:
                cv2.imshow('Camera', frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                text = pytesseract.image_to_string(img).strip()
                if text:
                    item_name = text.split('\n')[0]
            cap.release()
            settings = Settings()
            settings.load("user_settings.json")
            skin_tone = getattr(settings, "skin_tone", "medium")
            body_type = getattr(settings, "body_type", "average")
            # Color advice
            color_advice = ""
            color_map = {
                "fair": ["blue","red","white"],
                "medium": ["yellow","green","blue"],
                "dark": ["white","yellow","bright blue"]
            }
            preferred_colors = color_map.get(skin_tone, [])
            # Style advice
            style_map = {
                "slim": ["fitted", "layered", "straight"],
                "average": ["regular", "classic", "straight"],
                "curvy": ["a-line", "wrap", "high-waist", "flowy"],
                "athletic": ["structured", "tapered", "relaxed"]
            }
            preferred_styles = style_map.get(body_type, ["regular"])
            color_match = any(c in item_name.lower() for c in preferred_colors)
            style_match = any(s in item_name.lower() for s in preferred_styles)
            if item_name:
                advice = f"Scanned: {item_name}. "
                if color_match:
                    advice += "Color matches your skin tone. "
                else:
                    advice += "Color may not be ideal for your skin tone. "
                if style_match:
                    advice += "Style suits your body type. "
                else:
                    advice += "Style may not be ideal for your figure. "
                engine.say(advice)
                engine.runAndWait()
            else:
                engine.say("Could not detect item for shopping advice.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error giving shopping advice: {e}")
            engine.runAndWait()
    if "analyze my photo" in command or "analyze photo" in command:
        try:
            import cv2
            from PIL import Image
            import numpy as np
            from settings import Settings
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            skin_tone = "medium"
            body_type = "average"
            if ret:
                cv2.imshow('Camera', frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                np_img = np.array(img)
                # Estimate skin tone: sample center face region
                h, w, _ = np_img.shape
                face_region = np_img[h//4:h//2, w//3:2*w//3]
                avg_color = np.mean(face_region.reshape(-1,3), axis=0)
                # Simple skin tone logic
                if avg_color[0] > 200 and avg_color[1] > 180:
                    skin_tone = "fair"
                elif avg_color[0] > 120 and avg_color[1] > 100:
                    skin_tone = "medium"
                else:
                    skin_tone = "dark"
                # Estimate body type: aspect ratio
                aspect = w/h
                if aspect < 0.7:
                    body_type = "curvy"
                elif aspect < 0.85:
                    body_type = "average"
                elif aspect < 1.0:
                    body_type = "athletic"
                else:
                    body_type = "slim"
            # Update settings
            settings = Settings()
            settings.load("user_settings.json")
            settings.skin_tone = skin_tone
            settings.body_type = body_type
            settings.save("user_settings.json")
            engine.say(f"Estimated skin tone: {skin_tone}, body type: {body_type}. Settings updated for personalized outfit suggestions.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error analyzing photo: {e}")
            engine.runAndWait()
    if "scan my outfit" in command or "scan outfit" in command:
        try:
            import cv2, pytesseract, re, json
            from PIL import Image
            from settings import Settings
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            item_name = None
            if ret:
                cv2.imshow('Camera', frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                text = pytesseract.image_to_string(img).strip()
                if text:
                    item_name = text.split('\n')[0]
            cap.release()
            # Do NOT add detected item to wardrobe.json
            # Get weather info
            settings = Settings()
            settings.load("user_settings.json")
            city = settings.weather_city if hasattr(settings, "weather_city") else "London"
            weather_info = get_weather(city)
            match = re.match(r"(.+): ([\d.]+)°C, (.+)", weather_info)
            advice = ""
            if match:
                temp = float(match.group(2))
                desc = match.group(3).lower()
                # Basic advice based on temp and weather
                if temp < 5:
                    advice = "It's very cold. Make sure you are wearing warm layers."
                elif temp < 15:
                    advice = "It's cool. A jacket or sweater is recommended."
                elif temp < 25:
                    advice = "It's mild. Light layers should be fine."
                else:
                    advice = "It's warm. Light clothing is best."
                if "rain" in desc or "shower" in desc:
                    advice += " Don't forget an umbrella or raincoat."
                elif "snow" in desc:
                    advice += " Wear boots and warm layers for snow."
                elif "sun" in desc or "clear" in desc:
                    advice += " Sunglasses and sunscreen may be helpful."
            if item_name:
                engine.say(f"Detected: {item_name}. {weather_info}. {advice}")
                engine.runAndWait()
            else:
                engine.say(f"{weather_info}. {advice}")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error scanning outfit: {e}")
            engine.runAndWait()
    if "add clothing from camera" in command:
        try:
            import cv2, pytesseract, json
            from PIL import Image
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            item_name = None
            if ret:
                cv2.imshow('Camera', frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                text = pytesseract.image_to_string(img).strip()
                if text:
                    item_name = text.split('\n')[0]
            cap.release()
            if item_name:
                # Add to wardrobe.json
                try:
                    with open("wardrobe.json", "r", encoding="utf-8") as f:
                        wardrobe = json.load(f)
                except Exception:
                    wardrobe = []
                new_item = {"type": "unknown", "name": item_name, "warmth": "unknown", "rainproof": False}
                wardrobe.append(new_item)
                with open("wardrobe.json", "w", encoding="utf-8") as f:
                    json.dump(wardrobe, f, indent=2)
                engine.say(f"Added {item_name} to your wardrobe.")
                engine.runAndWait()
            else:
                engine.say("Could not detect clothing item from camera.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error adding clothing from camera: {e}")
            engine.runAndWait()
    if "what should i wear" in command or "what to wear" in command:
        try:
            from settings import Settings
            import json, re
            settings = Settings()
            settings.load("user_settings.json")
            city = settings.weather_city if hasattr(settings, "weather_city") else "London"
            weather_info = get_weather(city)
            match = re.match(r"(.+): ([\d.]+)°C, (.+)", weather_info)
            wardrobe_items = []
            try:
                with open("wardrobe.json", "r", encoding="utf-8") as f:
                    wardrobe_items = json.load(f)
            except Exception:
                wardrobe_items = []
            # Parse color and occasion from command
            color = None
            occasion = None
            color_words = ["blue","red","black","white","grey"]
            for c in color_words:
                if c in command:
                    color = c
                    break
            occasion_words = ["formal","casual","outdoor","event"]
            for o in occasion_words:
                if o in command:
                    occasion = o
                    break
            # Season detection
            import datetime
            month = datetime.datetime.now().month
            if month in [12,1,2]:
                season = "winter"
            elif month in [3,4,5]:
                season = "spring"
            elif month in [6,7,8]:
                season = "summer"
            else:
                season = "autumn"
            # Color mapping by skin tone and season
            skin_tone = getattr(settings, "skin_tone", "medium")
            preferred_colors = []
            if color is None:
                if skin_tone == "fair":
                    if season == "summer": preferred_colors = ["blue","red","white"]
                    elif season == "winter": preferred_colors = ["grey","black","navy"]
                    elif season == "spring": preferred_colors = ["pink","light blue","white"]
                    else: preferred_colors = ["brown","olive","burgundy"]
                elif skin_tone == "medium":
                    if season == "summer": preferred_colors = ["yellow","green","blue"]
                    elif season == "winter": preferred_colors = ["purple","grey","black"]
                    elif season == "spring": preferred_colors = ["coral","turquoise","white"]
                    else: preferred_colors = ["orange","olive","red"]
                else: # dark
                    if season == "summer": preferred_colors = ["white","yellow","bright blue"]
                    elif season == "winter": preferred_colors = ["emerald","navy","grey"]
                    elif season == "spring": preferred_colors = ["lavender","mint","white"]
                    else: preferred_colors = ["red","gold","brown"]
            # Use preferred color if not specified
            def color_match(item):
                if color:
                    return "color" in item and item["color"]==color
                elif preferred_colors:
                    return "color" in item and item["color"] in preferred_colors
                return True
            # Style mapping by body type
            body_type = getattr(settings, "body_type", "average")
            style_map = {
                "slim": ["fitted", "layered", "straight"],
                "average": ["regular", "classic", "straight"],
                "curvy": ["a-line", "wrap", "high-waist", "flowy"],
                "athletic": ["structured", "tapered", "relaxed"]
            }
            preferred_styles = style_map.get(body_type, ["regular"])
            def style_match(item):
                return "style" not in item or any(s in item["style"] for s in preferred_styles)
            if match:
                temp = float(match.group(2))
                desc = match.group(3).lower()
                # Select items based on temp, weather, color, occasion
                outfit = []
                for item in wardrobe_items:
                    # Weather logic
                    weather_match = False
                    if temp < 5 and item["warmth"]=="heavy":
                        weather_match = True
                    elif temp < 15 and item["warmth"] in ["medium","heavy"]:
                        weather_match = True
                    elif temp < 25 and item["warmth"] in ["light","medium"]:
                        weather_match = True
                    elif temp >= 25 and item["warmth"]=="light":
                        weather_match = True
                    if "rain" in desc or "shower" in desc:
                        if item["rainproof"]:
                            weather_match = True
                    if "snow" in desc:
                        if item["type"]=="boots" and item["warmth"]=="heavy":
                            weather_match = True
                    if "sun" in desc or "clear" in desc:
                        if item["type"]=="sunglasses":
                            weather_match = True
                    # Color and occasion logic
                    occasion_match = occasion is None or ("occasion" in item and occasion in item["occasion"])
                    if weather_match and color_match(item) and occasion_match and style_match(item):
                        outfit.append(item["name"])
                # Remove duplicates
                outfit = list(dict.fromkeys(outfit))
                suggestion = ", ".join(outfit) if outfit else "No matching items found in your wardrobe."
                engine.say(f"{weather_info}. Suggested outfit: {suggestion}")
                engine.runAndWait()
            else:
                engine.say(f"{weather_info}. Unable to give outfit advice.")
                engine.runAndWait()
        except Exception as e:
            engine.say(f"Error giving outfit advice: {e}")
            engine.runAndWait()
    command = command.lower()
    if "read screen" in command:
        engine.say("Reading screen now.")
        engine.runAndWait()
        read_screen()
    elif "set weather city to" in command:
        city = command.split("set weather city to",1)[1].strip()
        try:
            from settings import Settings
            settings = Settings()
            settings.load("user_settings.json")
            settings.weather_city = city
            settings.save("user_settings.json")
            engine.say(f"Weather city set to {city} and saved.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error saving weather city: {e}")
            engine.runAndWait()
    elif "weather" in command:
        try:
            from settings import Settings
            settings = Settings()
            settings.load("user_settings.json")
            city = settings.weather_city if hasattr(settings, "weather_city") else "London"
            weather_info = get_weather(city)
            engine.say(weather_info)
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting weather: {e}")
            engine.runAndWait()
    elif "note" in command:
        engine.say("Creating a new note.")
        engine.runAndWait()
        try:
            create_note()
        except Exception as e:
            engine.say(f"Error creating note: {e}")
            engine.runAndWait()
    elif "remote" in command:
        engine.say("Performing remote control action.")
        engine.runAndWait()
        try:
            remote_action(command)
        except Exception as e:
            engine.say(f"Error in remote control: {e}")
            engine.runAndWait()
    elif "joke" in command:
        engine.say("Here's a joke.")
        engine.runAndWait()
        try:
            joke = tell_joke()
            engine.say(joke)
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error telling joke: {e}")
            engine.runAndWait()
    elif "fitness" in command:
        engine.say("Getting fitness stats.")
        engine.runAndWait()
        try:
            stats = get_fitness_stats()
            engine.say(str(stats))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting fitness stats: {e}")
            engine.runAndWait()
    elif "calendar" in command:
        engine.say("Syncing calendar.")
        engine.runAndWait()
        try:
            sync_user_calendar()
        except Exception as e:
            engine.say(f"Error syncing calendar: {e}")
            engine.runAndWait()
    elif "medication" in command:
        engine.say("Reminding medication.")
        engine.runAndWait()
        try:
            remind_medication()
        except Exception as e:
            engine.say(f"Error with medication reminder: {e}")
            engine.runAndWait()
    elif "emergency contact" in command:
        engine.say("Getting emergency contacts.")
        engine.runAndWait()
        try:
            contacts = get_emergency_contacts()
            engine.say(str(contacts))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting emergency contacts: {e}")
            engine.runAndWait()
    elif "expense" in command:
        engine.say("Getting expense summary.")
        engine.runAndWait()
        try:
            summary = get_expense_summary()
            engine.say(str(summary))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting expense summary: {e}")
            engine.runAndWait()
    elif "file" in command:
        engine.say("Searching files.")
        engine.runAndWait()
        try:
            result = search_files(command)
            engine.say(str(result))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error searching files: {e}")
            engine.runAndWait()
    elif "camera" in command:
        engine.say("Capturing and reading text from camera.")
        engine.runAndWait()
        try:
            capture_and_read_text()
        except Exception as e:
            engine.say(f"Error with camera: {e}")
            engine.runAndWait()
    elif "scan document" in command:
        engine.say("Scanning document.")
        engine.runAndWait()
        try:
            scan_document()
        except Exception as e:
            engine.say(f"Error scanning document: {e}")
            engine.runAndWait()
    elif "dashboard" in command:
        engine.say("Getting dashboard widgets.")
        engine.runAndWait()
        try:
            widgets = get_dashboard_widgets()
            engine.say(str(widgets))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting dashboard: {e}")
            engine.runAndWait()
    elif "shortcut" in command:
        engine.say("Listing shortcuts.")
        engine.runAndWait()
        try:
            shortcuts = list_shortcuts()
            engine.say(str(shortcuts))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error listing shortcuts: {e}")
            engine.runAndWait()
    elif "contact" in command:
        engine.say("Getting contact info.")
        engine.runAndWait()
        try:
            info = get_contact_info(command, "info")
            engine.say(str(info))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting contact info: {e}")
            engine.runAndWait()
    elif "call" in command:
        engine.say("Calling contact.")
        engine.runAndWait()
        try:
            # Example: call_phone_twilio(to_number, from_number, twilio_sid, twilio_token)
            engine.say("Call function triggered.")
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error making call: {e}")
            engine.runAndWait()
    elif "language" in command:
        engine.say("Starting language learning.")
        engine.runAndWait()
        try:
            daily_vocabulary()
        except Exception as e:
            engine.say(f"Error with language learning: {e}")
            engine.runAndWait()
    elif "location" in command:
        engine.say("Getting location.")
        engine.runAndWait()
        try:
            loc = get_location()
            engine.say(str(loc))
            engine.runAndWait()
        except Exception as e:
            engine.say(f"Error getting location: {e}")
            engine.runAndWait()
    elif "media" in command:
        engine.say("Playing media.")
        engine.runAndWait()
        try:
            play_media(command)
        except Exception as e:
            engine.say(f"Error playing media: {e}")
            engine.runAndWait()
    else:
        engine.say("Command not recognized. Please try again.")
        engine.runAndWait()


def listen_for_commands():
    recognizer = sr.Recognizer()
    print("\n--- Microphone Diagnostics ---")
    mic_names = sr.Microphone.list_microphone_names()
    if not mic_names:
        print("No microphones detected. Please check your device connection and drivers.")
        engine.say("No microphones detected. Please check your device connection and drivers.")
        engine.runAndWait()
        return
    print("Available microphones:")
    for idx, name in enumerate(mic_names):
        print(f"  {idx}: {name}")
    # Try to use default mic, or let user select
    try:
        mic = sr.Microphone()
        print(f"Using default microphone: {mic_names[mic.device_index]}")
    except Exception as e:
        print(f"Microphone error: {e}")
        engine.say(f"Microphone error: {e}")
        engine.runAndWait()
        print("If you have multiple microphones, try specifying a device index:")
        for idx, name in enumerate(mic_names):
            print(f"  sr.Microphone(device_index={idx}) for {name}")
        return

    engine.say("Say a command, like 'read screen', 'weather', 'note', or 'remote'.")
    engine.runAndWait()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        handle_voice_command(command)
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase.")
        engine.say("Listening timed out. Please try again.")
        engine.runAndWait()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        engine.say("Could not understand audio. Please speak clearly.")
        engine.runAndWait()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        engine.say(f"Speech recognition service error: {e}")
        engine.runAndWait()
    except Exception as e:
        print(f"General error: {e}")
        engine.say(f"Could not process command: {e}")
        engine.runAndWait()
