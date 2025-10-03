import threading
import time
def start_real_time_navigation(destination, speak_func):
    """
    Continuously monitor GPS and announce turns as user approaches them.
    speak_func: function to speak instructions (e.g., pyttsx3 or gTTS)
    """
    steps = get_directions(destination)
    # For GPS proximity, you need step coordinates from OpenRouteService
    # This demo assumes each step is a dict with 'instruction' and 'way_points' (index into route geometry)
    import geocoder
    def get_current_coords():
        g = geocoder.osm('me')
        if g.latlng:
            return g.latlng
        return None
    def nav_thread():
        announced = set()
        while True:
            coords = get_current_coords()
            if coords:
                lat, lon = coords
                # For each step, check proximity (within ~30 meters)
                for i, step in enumerate(steps):
                    # If step is just instruction string, skip proximity
                    if isinstance(step, str):
                        continue
                    step_latlon = step.get('location')  # Should be [lat, lon]
                    if step_latlon and i not in announced:
                        dist = ((lat-step_latlon[0])**2 + (lon-step_latlon[1])**2)**0.5 * 111000  # rough meters
                        if dist < 30:
                            speak_func(step['instruction'])
                            announced.add(i)
            time.sleep(5)
    t = threading.Thread(target=nav_thread, daemon=True)
    t.start()
# location.py
# Location services feature

import geocoder
from geopy.geocoders import Nominatim

def get_location():
    try:
        # Try GPS first (if available)
        import geocoder
        g = geocoder.osm('me')
        if g.latlng:
            geolocator = Nominatim(user_agent="talkback_assistant")
            location = geolocator.reverse(f"{g.latlng[0]}, {g.latlng[1]}")
            if location and 'city' in location.raw['address']:
                return location.raw['address']['city']
        # Fallback to IP geolocation
        g_ip = geocoder.ip('me')
        if g_ip.city:
            return g_ip.city
        return "London"
    except Exception as e:
        print(f"Location error: {e}")
        return "London"

def get_directions(destination):
    try:
        origin = get_location()
        import requests
        # Choose mode: 'car', 'foot', 'public_transport'
        mode = 'foot'  # Default
        import sys
        if hasattr(sys, 'argv') and len(sys.argv) > 2:
            mode = sys.argv[2]
        # Get coordinates for origin and destination
        url_dest = f"https://nominatim.openstreetmap.org/search?format=json&q={destination}"
        resp_dest = requests.get(url_dest)
        data_dest = resp_dest.json()
        url_origin = f"https://nominatim.openstreetmap.org/search?format=json&q={origin}"
        resp_origin = requests.get(url_origin)
        data_origin = resp_origin.json()
        if data_dest and data_origin:
            orig_lat = float(data_origin[0]["lat"])
            orig_lon = float(data_origin[0]["lon"])
            dest_lat = float(data_dest[0]["lat"])
            dest_lon = float(data_dest[0]["lon"])
            ORS_API_KEY = "YOUR_OPENROUTESERVICE_API_KEY"
            headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
            if mode == 'car':
                route_url = "https://api.openrouteservice.org/v2/directions/driving-car"
            elif mode == 'public_transport':
                # Detect country/city for API selection
                import geopy
                from geopy.geocoders import Nominatim
                geolocator = Nominatim(user_agent="talkback_assistant")
                location_info = geolocator.geocode(origin)
                country = getattr(location_info, 'address', '').split(',')[-1].strip() if location_info else ''
                city = getattr(location_info, 'address', '').split(',')[0].strip() if location_info else ''
                # UK APIs
                if country == 'United Kingdom':
                    # TransportAPI integration
                    # Register at https://www.transportapi.com/ for free app_id and app_key
                    import os
                    app_id = os.environ.get("TRANSPORTAPI_APP_ID", "YOUR_APP_ID")
                    app_key = "ecaa31d3fbff21bd52f13b938e53d95c"
                    url = f"https://transportapi.com/v3/uk/public/journey/from/{orig_lat},{orig_lon}/to/{dest_lat},{dest_lon}.json?app_id={app_id}&app_key={app_key}"
                    try:
                        resp = requests.get(url)
                        data = resp.json()
                        steps_out = []
                        for leg in data.get("journeys", [{}])[0].get("legs", []):
                            mode = leg.get("mode", "")
                            dep = leg.get("departure_point", {}).get("name", "")
                            arr = leg.get("arrival_point", {}).get("name", "")
                            dep_time = leg.get("departure_time", "")
                            arr_time = leg.get("arrival_time", "")
                            service = leg.get("service", {}).get("number", "")
                            platform = leg.get("departure_point", {}).get("platform", "")
                            step_str = f"Take {mode} {service} from {dep}"
                            if platform:
                                step_str += f", Platform {platform}"
                            step_str += f" at {dep_time}. Arrive at {arr} at {arr_time}."
                            steps_out.append(step_str)
                        if steps_out:
                            return steps_out
                        else:
                            return ["No UK public transport route found for your destination."]
                    except Exception as e:
                        return [f"Error fetching UK public transport: {e}"]
                # London TfL
                if city.lower() == 'london':
                    # TfL API (stub)
                    # See https://api.tfl.gov.uk/
                    return ["London TfL API integration required. See docs for setup."]
                # Germany (Berlin/Brandenburg)
                if city.lower() in ['berlin', 'brandenburg']:
                    # VBB API integration stub
                    # Register and get credentials at https://www.vbb.de/en/article/traffic-data/
                    # Example:
                    # import requests
                    # url = f"https://vbb.transport.rest/journeys?from={orig_lat},{orig_lon}&to={dest_lat},{dest_lon}"
                    # resp = requests.get(url)
                    # data = resp.json()
                    # Parse and return steps
                    return ["Berlin/Brandenburg VBB API: Add credentials and complete integration."]
                # France (SNCF)
                if country == 'France':
                    # SNCF API integration stub
                    # Register and get credentials at https://www.digital.sncf.com/startup/api
                    # Example:
                    # import requests
                    # url = f"https://api.sncf.com/v1/coverage/sncf/journeys?from={orig_lat},{orig_lon}&to={dest_lat},{dest_lon}&key=YOUR_SNCF_KEY"
                    # resp = requests.get(url)
                    # data = resp.json()
                    # Parse and return steps
                    return ["France SNCF API: Add credentials and complete integration."]
                # Switzerland
                if country == 'Switzerland':
                    # OpenTransportData API integration stub
                    # Register and get credentials at https://www.opentransportdata.swiss/en/
                    # Example:
                    # import requests
                    # url = f"https://api.opentransportdata.swiss/...?from={orig_lat},{orig_lon}&to={dest_lat},{dest_lon}&key=YOUR_SWISS_KEY"
                    # resp = requests.get(url)
                    # data = resp.json()
                    # Parse and return steps
                    return ["Swiss OpenTransportData API: Add credentials and complete integration."]
                # Belgium
                if country == 'Belgium':
                    # De Lijn API integration stub
                    # Register and get credentials at https://data.delijn.be/
                    # Example:
                    # import requests
                    # url = f"https://api.delijn.be/...?from={orig_lat},{orig_lon}&to={dest_lat},{dest_lon}&key=YOUR_DELijn_KEY"
                    # resp = requests.get(url)
                    # data = resp.json()
                    # Parse and return steps
                    return ["Belgium De Lijn API: Add credentials and complete integration."]
                # Austria
                if country == 'Austria':
                    # OEBB API integration stub
                    # Register and get credentials at https://www.oebb.at/en/unternehmen/Services-fuer-Partner/Open-Data.html
                    # Example:
                    # import requests
                    # url = f"https://api.oebb.at/...?from={orig_lat},{orig_lon}&to={dest_lat},{dest_lon}&key=YOUR_OEBB_KEY"
                    # resp = requests.get(url)
                    # data = resp.json()
                    # Parse and return steps
                    return ["Austria OEBB API: Add credentials and complete integration."]
                # Fallback to OpenRouteService public transport
                ORS_API_KEY = "YOUR_OPENROUTESERVICE_API_KEY"
                headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}
                ors_url = "https://api.openrouteservice.org/v2/directions/public-transport"
                body = {"coordinates": [[orig_lon, orig_lat], [dest_lon, dest_lat]]}
                try:
                    ors_resp = requests.post(ors_url, json=body, headers=headers)
                    ors_data = ors_resp.json()
                    if "features" in ors_data and ors_data["features"]:
                        steps = ors_data["features"][0]["properties"]["segments"][0]["steps"]
                        return [step["instruction"] for step in steps]
                except Exception:
                    pass
                # Fallback to Google Transit Directions API
                import os
                GOOGLE_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY")
                origin_str = f"{orig_lat},{orig_lon}"
                dest_str = f"{dest_lat},{dest_lon}"
                transit_url = (
                    f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_str}&destination={dest_str}&mode=transit&key={GOOGLE_API_KEY}"
                )
                try:
                    transit_resp = requests.get(transit_url)
                    transit_data = transit_resp.json()
                    steps_out = []
                    routes = transit_data.get("routes", [])
                    if routes:
                        legs = routes[0].get("legs", [])
                        for leg in legs:
                            for step in leg.get("steps", []):
                                travel_mode = step.get("travel_mode", "")
                                if travel_mode == "TRANSIT":
                                    transit_details = step.get("transit_details", {})
                                    line = transit_details.get("line", {})
                                    vehicle = line.get("vehicle", {}).get("type", "")
                                    line_name = line.get("short_name", line.get("name", ""))
                                    departure_stop = transit_details.get("departure_stop", {}).get("name", "")
                                    arrival_stop = transit_details.get("arrival_stop", {}).get("name", "")
                                    departure_time = transit_details.get("departure_time", {}).get("text", "")
                                    arrival_time = transit_details.get("arrival_time", {}).get("text", "")
                                    platform = transit_details.get("departure_platform", "")
                                    step_str = f"Take {vehicle.lower()} {line_name} from {departure_stop}"
                                    if platform:
                                        step_str += f", Platform {platform}"
                                    step_str += f" at {departure_time}. Arrive at {arrival_stop} at {arrival_time}."
                                    steps_out.append(step_str)
                                else:
                                    instruction = step.get("html_instructions", "")
                                    steps_out.append(instruction)
                        if steps_out:
                            return steps_out
                    return ["No transit route found for your destination."]
                except Exception as e:
                    return [f"Error fetching Google transit directions: {e}"]
            else:
                route_url = "https://api.openrouteservice.org/v2/directions/foot-walking"
            body = {
                "coordinates": [[orig_lon, orig_lat], [dest_lon, dest_lat]]
            }
            route_resp = requests.post(route_url, json=body, headers=headers)
            route_data = route_resp.json()
            if "features" in route_data and route_data["features"]:
                steps = route_data["features"][0]["properties"]["segments"][0]["steps"]
                return [step["instruction"] for step in steps]
            else:
                return [f"Could not get turn-by-turn directions, but your destination is at latitude {dest_lat}, longitude {dest_lon}."]
        else:
            return [f"Could not find directions to {destination}."]
    except Exception as e:
        return [f"Error getting directions: {e}"]
