# dashboard.py
# Customizable dashboard feature

def get_dashboard_widgets():
    # TODO: Get dashboard widgets
    return []


def set_dashboard_widget(widget):
    # TODO: Set dashboard widget
    pass

# New: Get map directions to a spoken place
def get_map_directions_by_speech():
    from speech import listen, speak
    import requests
    speak("Where do you want directions to?")
    place = listen("en")
    if not place:
        speak("No place detected.")
        return None
    # Use Google Maps Directions API (requires API key)
    api_key = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your actual key
    origin = "current location"  # You can use device location if available
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={place}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("routes"):
            steps = data["routes"][0]["legs"][0]["steps"]
            directions = []
            for step in steps:
                directions.append(step["html_instructions"])
            speak("Directions:")
            for d in directions:
                speak(d)
            return directions
        else:
            speak("No directions found.")
            return None
    else:
        speak("Failed to get directions.")
        return None
