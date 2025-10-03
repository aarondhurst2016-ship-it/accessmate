# weather_alerts.py
# Weather alerts feature

import requests

def get_weather_alerts(city="London"):
    # Example using OpenWeatherMap API (replace with your API key)
    API_KEY = "your_openweathermap_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        alerts = []
        # OpenWeatherMap returns alerts in 'weather' key
        if 'weather' in data:
            for alert in data['weather']:
                alerts.append(alert.get('description', 'No description'))
        return alerts
    except Exception as e:
        print(f"Weather alert error: {e}")
        return []
