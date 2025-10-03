# Weather API integration for Kivy (mobile/desktop)
import requests

API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if 'main' in data:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{city}: {temp}°C, {desc}"
        else:
            return f"Weather not found for {city}"
    except Exception as e:
        return f"Weather error: {e}"
