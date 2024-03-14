# https://rapidapi.com/DataCrawler/api/tripadvisor16/

import requests

def get_lat_lng(address):
    url = f"http://nominatim.openstreetmap.org/search?format=json&q={address}"
    response = requests.get(url).json()
    return float(response[0]['lat']), float(response[0]['lon'])

address = 'Stadio Euganeo, Padova, Italy'

lat, lon = get_lat_lng(address)

url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchHotelsByLocation"

querystring = {"latitude":lat,"longitude":lon,"checkIn":"2024-03-10","checkOut":"2024-03-11","pageNumber":"1","currencyCode":"USD"}

headers = {
    "X-RapidAPI-Key": "75aac3e5e6msh766d172130c50a3p1b0935jsn5d859f219ac6",
    "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())