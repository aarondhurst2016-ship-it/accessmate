def read_file(filepath):
    print(f"Reading file: {filepath}")
    return "File content"

def write_file(filepath, text):
    print(f"Writing to file: {filepath}")
    return True

def is_valid_email(email):
    return "@" in email

def format_datetime():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Accessibility helper for Kivy
def enable_accessibility(widget, tooltip=None):
    if tooltip:
        widget.bind(on_focus=lambda instance, value: print(f"Tooltip: {tooltip}") if value else None)
