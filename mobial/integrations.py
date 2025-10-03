from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import sys
import os

def send_sms_twilio(to_number, message, from_number, account_sid, auth_token):
    try:
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_number, to=to_number)
        print(f"SMS sent to {to_number}")
    except Exception as e:
        print(f"Twilio SMS error: {e}")

def scrape_webpage(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string if soup.title else "No title found"
    except Exception as e:
        print(f"Web scraping error: {e}")
        return None

def generate_pdf(text, filename="output.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.cell(200, 10, txt=line, ln=1)
        pdf.output(filename)
        print(f"PDF generated: {filename}")
    except Exception as e:
        print(f"PDF generation error: {e}")

def open_mobile_app(app_id_or_url):
    if sys.platform == 'android':
        # Android: use os.system to call am start
        try:
            os.system(f'am start -n {app_id_or_url}')
        except Exception as e:
            print(f"Error launching Android app: {e}")
    elif sys.platform == 'ios':
        # iOS: use URL scheme
        import webbrowser
        try:
            webbrowser.open(app_id_or_url)
        except Exception as e:
            print(f"Error launching iOS app: {e}")
    else:
        print("Mobile app launching only supported on Android/iOS.")
