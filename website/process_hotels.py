import json
from compute_distance import get_lat_lng, calculate_distance
from concurrent.futures import ThreadPoolExecutor
import time


def process_hotel_data(data, destination_address=None, retries=5):
    """
    Extracts and formats hotel information from a JSON response,
    calculating distance concurrently and handling potential failures.

    Args:
        data (dict): The JSON data containing hotel information.
        destination_address (str): The address to calculate distance to (optional).
        retries (int): Number of retries for calculate_distance (default: 3).

    Returns:
        list: A list of dictionaries, where each dictionary represents a hotel
              with its details, including distance if provided.
    """
    hotels = []
    with ThreadPoolExecutor() as executor:
        # Define function to process a single hotel
        def process_hotel(hotel):
            hotel_info = {
                "name": hotel['title'],
                "address": f"{hotel['secondaryInfo']}",  # Assuming secondaryInfo contains address details
                "price": hotel["priceForDisplay"],
                "photos": [photo["sizes"]["urlTemplate"] for photo in hotel["cardPhotos"]],
                "hotel_url": hotel["commerceInfo"]["externalUrl"],
                "provider": hotel["commerceInfo"]["provider"],
                "rating": hotel["bubbleRating"]["rating"],
            }
            if destination_address:
                for attempt in range(retries):
                    try:
                        hotel_info['distance'] = calculate_distance(hotel_info['address'], destination_address)
                        break  # Exit loop on successful calculation
                    except:
                        hotel_info['distance'] = None
                        time.sleep(1)  # Add a slight delay between retries
            return hotel_info

        # Submit hotel processing tasks to the thread pool
        hotel_futures = executor.map(process_hotel, data["data"]["data"])

        # Collect results from completed tasks
        for hotel_info in hotel_futures:
            hotels.append(hotel_info)

    return hotels


# Example usage
filename = 'sample_hotels.json'  # Replace with your actual filename
with open(filename, 'r') as file:
    data = json.load(file)
destination_address = 'Stadio Euganeo, Padova'

# Process and print hotel information
hotels = process_hotel_data(data, destination_address)
for hotel in hotels:
    print(f"Name: {hotel['name']}")
    print(f"Address: {hotel['address']}")
    print(f"Price: {hotel['price']}")
    print(f"Photos:")
    for photo_url in hotel['photos']:
        print(f"- {photo_url}")
    print(f"Hotel URL: {hotel['hotel_url']}")
    print(f"Provider: {hotel['provider']}")
    print(f"Rating: {hotel['rating']}")
    print(f"Distance: {hotel['distance']}")
    print("-" * 30)