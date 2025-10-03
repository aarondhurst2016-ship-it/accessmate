"""
ai_assistant.py - Unified AI assistant handler
Routes user input to AI chat or feature modules (screen reading, weather, notes, etc.)
"""
from ai_chat import chat_with_gpt
from screen_reader import read_screen, read_foreground_window, read_all_windows, read_selected_text
from weather import get_weather
from notes import create_note
from remote_control import control_device

# Add more imports for your features as needed

def handle_user_input(user_input):
    """
    Unified handler: routes input to features or AI chat.
    Returns response string.
    """
    command = user_input.lower().strip()
    # Feature triggers (expand as needed)
    if "read screen" in command:
        return read_screen() or "Nothing to read on screen."
    elif "read window" in command or "read foreground" in command:
        return read_foreground_window() or "Nothing to read in window."
    elif "read all windows" in command:
        return read_all_windows() or "Nothing to read in windows."
    elif "read selected" in command or "read clipboard" in command:
        return read_selected_text() or "Nothing selected."
    elif "weather" in command:
        return get_weather()
    elif "note" in command:
        create_note()
        return "Note created."
    elif "control" in command:
        # Example: "control light on" or "control tv off"
        parts = command.split()
        if len(parts) >= 3:
            device = parts[1]
            action = parts[2]
            return control_device(device, action)
        else:
            return "Specify device and action."
    # Add more feature triggers here
    else:
        # Fallback: AI chat
        return chat_with_gpt(user_input)

if __name__ == "__main__":
    print("Unified AI Assistant. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "quit":
            break
        reply = handle_user_input(user_input)
        print(f"Assistant: {reply}")
