"""
call_integration.py - Call via phone, WhatsApp, Messenger, or other methods
"""
import sys
import webbrowser
import platform
import os
from contacts import get_contact_info

def call_phone_twilio(to_number, from_number, twilio_sid, twilio_token):
    """Make a phone call using Twilio API. Accepts contact name or number."""
    if not to_number.startswith("+"):
        contact_num = get_contact_info(to_number, "phone")
        if contact_num:
            to_number = contact_num
    try:
        from twilio.rest import Client
        client = Client(twilio_sid, twilio_token)
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        print(f"Call initiated: {call.sid}")
        return True
    except Exception as e:
        print(f"Twilio call failed: {e}")
        return False

def open_whatsapp(phone_number, message=""):
    """Open WhatsApp chat with a contact name or phone number and optional message."""
    if not phone_number.startswith("+"):
        contact_num = get_contact_info(phone_number, "whatsapp")
        if contact_num:
            phone_number = contact_num
    url = f"https://wa.me/{phone_number}?text={message}"
    webbrowser.open(url)
    print(f"Opened WhatsApp for {phone_number}")

def open_messenger(user_id):
    """Open Facebook Messenger chat with a contact name or user ID."""
    contact_id = get_contact_info(user_id, "messenger")
    if contact_id:
        user_id = contact_id
    url = f"https://m.me/{user_id}"
    webbrowser.open(url)
    print(f"Opened Messenger for user {user_id}")

def open_phone_dialer(phone_number):
    """Open the default phone dialer with a contact name or number (mobile/desktop)."""
    if not phone_number.startswith("+"):
        contact_num = get_contact_info(phone_number, "phone")
        if contact_num:
            phone_number = contact_num
    import sys
    # Mobile platform detection
    if hasattr(sys, 'getandroidapilevel') or 'ANDROID_ARGUMENT' in os.environ:
        # Android: use os.system with am start
        os.system(f"am start -a android.intent.action.DIAL -d tel:{phone_number}")
        print(f"Opened Android dialer for {phone_number}")
    elif sys.platform == "ios" or 'IOS_ARGUMENT' in os.environ:
        # iOS: use webbrowser to open tel: URL
        webbrowser.open(f"tel://{phone_number}")
        print(f"Opened iOS dialer for {phone_number}")
    elif platform.system() == "Windows":
        os_command = f"start tel:{phone_number}"
        os.system(os_command)
        print(f"Opened Windows dialer for {phone_number}")
    elif platform.system() == "Darwin":
        os.system(f"open 'tel:{phone_number}'")
        print(f"Opened macOS dialer for {phone_number}")
    elif platform.system() == "Linux":
        os.system(f"xdg-open 'tel:{phone_number}'")
        print(f"Opened Linux dialer for {phone_number}")
    else:
        webbrowser.open(f"tel:{phone_number}")
        print(f"Opened generic dialer for {phone_number}")

# Example usage:
# call_phone_twilio('+1234567890', '+1098765432', 'TWILIO_SID', 'TWILIO_TOKEN')
# open_whatsapp('1234567890', 'Hello!')
# open_messenger('user_id')
# open_phone_dialer('1234567890')
