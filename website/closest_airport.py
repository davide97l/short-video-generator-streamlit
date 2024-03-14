from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
from geopy import Point
import requests
import json

def find_closest_airport(location=None, coordinates=None):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        if location:
            location = geolocator.geocode(location)
            lat, lon = location.latitude, location.longitude
        elif coordinates:
            lat, lon = coordinates[0], coordinates[1]
        else:
            return "You must provide a location or coordinates"

    except GeocoderTimedOut:
        return "GeocoderTimedOut: geocode failed on input %s with message %s" % (location)

    base_url = "http://api.geonames.org/findNearbyJSON?lat={}&lng={}&fcode=AIRP&radius=100&username=demo"
    response = requests.get(base_url.format(lat, lon))
    data = response.json()
    print(data)

    airports = {}

    for airport in data['geonames']:
        airport_loc = (airport['lat'], airport['lng'])
        if coordinates:
            dist = geodesic(Point(coordinates), airport_loc).km
        else:
            dist = geodesic((lat, lon), airport_loc).km
        airports[airport['name']] = dist

    closest_airport = min(airports, key=airports.get)

    return closest_airport

# Test with name of city
print(find_closest_airport(location="New York"))

# Test with coordinates
print(find_closest_airport(coordinates=(40.712776, -74.005974)))