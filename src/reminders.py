
# Reminders and appointments backend
import json
import os
import uuid
from datetime import datetime

REMINDER_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    try:
        with open(REMINDER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_reminders(reminders):
    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(user, title, description, dt, recurrence=None, type_="reminder"):
    reminders = load_reminders()
    reminder = {
        "id": str(uuid.uuid4()),
        "user": user,
        "type": type_,  # 'reminder' or 'appointment'
        "title": title,
        "description": description,
        "datetime": dt,
        "recurrence": recurrence,  # e.g., 'daily', 'weekly', None
        "notified": False
    }
    reminders.append(reminder)
    save_reminders(reminders)
    return reminder["id"]

def get_reminders(user=None, upcoming_only=False):
    reminders = load_reminders()
    now = datetime.now().isoformat()
    result = []
    for r in reminders:
        if user and r["user"] != user:
            continue
        if upcoming_only and r["datetime"] < now:
            continue
        result.append(r)
    return result

def update_reminder(reminder_id, **kwargs):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r.update(kwargs)
            save_reminders(reminders)
            return True
    return False

def delete_reminder(reminder_id):
    reminders = load_reminders()
    reminders = [r for r in reminders if r["id"] != reminder_id]
    save_reminders(reminders)

def set_reminder(text, time, user="local"):
    """Legacy: Add a simple reminder for compatibility."""
    return add_reminder(user, text, text, time, None, "reminder")

def list_reminders(user="local"):
    return get_reminders(user)
