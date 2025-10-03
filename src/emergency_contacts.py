# emergency_contacts.py
# Emergency contacts feature

import json
import os

CONTACTS_FILE = os.path.join(os.path.dirname(__file__), '../user_settings.json')

def add_emergency_contact(name, number):
    contacts = []
    # Load existing contacts
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            try:
                data = json.load(f)
                contacts = data.get('emergency_contacts', [])
            except Exception:
                contacts = []
    # Add new contact
    contacts.append({'name': name, 'number': number})
    # Save back
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
    else:
        data = {}
    data['emergency_contacts'] = contacts
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_emergency_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data.get('emergency_contacts', [])
            except Exception:
                return []
    return []
