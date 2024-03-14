import requests
import math
import time


def get_lat_lng(address):
    url = f"http://nominatim.openstreetmap.org/search?format=json&q={address}"
    response = requests.get(url).json()
    return float(response[0]['lat']), float(response[0]['lon'])


def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # radius of Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    res = r * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))
    return res  # distance in kilometers


def calculate_distance(address1, address2):
    lat1, lon1 = get_lat_lng(address1)
    lat2, lon2 = get_lat_lng(address2)
    return haversine(lat1, lon1, lat2, lon2)


if __name__ == 'main':
    # Tests
    test_cases = [
        {"address1": "Prato della Valle, Padova", "address2": "Stadio Euganeo, Padova", "expected": 4.0},
        {"address1": "The White House, Washington, D.C.", "address2": "Times Square, New York, NY", "expected": 332.5},
    ]

    # Initialize a counter for passed tests and a list to collect all latencies
    passed_tests = 0
    total_latency = 0

    # Run the tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['address1']} to {test_case['address2']}")
        expected_distance = test_case['expected']

        start_time = time.time()
        lat1, lon1 = get_lat_lng(test_case['address1'])
        lat2, lon2 = get_lat_lng(test_case['address2'])
        latency = time.time() - start_time
        total_latency += latency

        actual_distance = haversine(lat1, lon1, lat2, lon2)
        print("Expected ~", expected_distance, "km")
        print("Result:", actual_distance, "km")
        print("Latency:", latency, "seconds")
        test_passed = math.isclose(expected_distance, actual_distance, abs_tol=0.5)
        print("Passes test:", test_passed, "\n")

        if test_passed:
            passed_tests += 1

    average_latency = total_latency / len(test_cases)
    print(f"{passed_tests} out of {len(test_cases)} tests passed.")
    print("Average latency:", average_latency, "seconds")