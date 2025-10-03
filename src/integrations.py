# External integrations for Talkback Assistant
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

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

def integrate_service(service_name):
    if service_name.lower() == "twilio":
        # Example usage: send_sms_twilio("+1234567890", "Hello!", "YOUR_TWILIO_NUMBER", "YOUR_SID", "YOUR_TOKEN")
        print("Twilio integration ready. Call send_sms_twilio().")
    elif service_name.lower() == "web":
        print("Web scraping integration ready. Call scrape_webpage().")
    elif service_name.lower() == "pdf":
        print("PDF generation ready. Call generate_pdf().")
    else:
        print(f"No integration for {service_name}")
