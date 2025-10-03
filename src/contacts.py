# contacts.py - Simple contact name to number/user mapping
CONTACTS = {
    "Alice": {
        "phone": "+1234567890",
        "whatsapp": "+1234567890",
        "messenger": "alice.fb.id"
    },
    "Bob": {
        "phone": "+1098765432",
        "whatsapp": "+1098765432",
        "messenger": "bob.fb.id"
    }
    # Add more contacts as needed
}

def get_contact_info(name, method):
    info = CONTACTS.get(name)
    if info:
        return info.get(method)
    return None
