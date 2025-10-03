# Weather API integration for Tkinter (desktop)
import requests

API_KEY = '42784e3ba5d1d0b81ee88fc5c67db19b'

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
