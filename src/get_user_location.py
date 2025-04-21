import requests

def get_user_location_by_ip():
    """Get the user's latitude and longitude based on their IP address."""
    try:
        # Use ipinfo.io to get location data
        response = requests.get("https://ipinfo.io/json")
        if response.status_code != 200:
            raise Exception("Failed to fetch location data")

        data = response.json()
        if 'loc' not in data:
            raise Exception("Location data not available in the response")

        # Extract latitude and longitude
        loc = data['loc'].split(',')
        latitude = float(loc[0])
        longitude = float(loc[1])

        return latitude, longitude
    except Exception as e:
        print(f"Error fetching user location: {e}")
        return None, None

if __name__ == "__main__":
    lat, lng = get_user_location_by_ip()
    if lat is not None and lng is not None:
        print(f"Your location: Latitude = {lat}, Longitude = {lng}")
    else:
        print("Could not determine your location.")