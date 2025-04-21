import requests
import os
from dotenv import load_dotenv
from get_user_location import get_user_location_by_ip

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
#load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set")


def get_nearby_stores(radius_miles=5, store_type='grocery_or_supermarket'):
    """Fetch nearby grocery stores and sort by rating."""
    lat, lng = get_user_location_by_ip()

    radius_meters = int(radius_miles * 1609.34)  # convert miles to meters
    endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    params = {
        'location': f'{lat},{lng}',
        'radius': radius_meters,
        'type': store_type,
        'key': GOOGLE_MAPS_API_KEY
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'results' not in data:
        raise Exception("No results found or invalid API response")

    stores = []
    for place in data['results']:
        stores.append({
            'name': place.get('name'),
            'address': place.get('vicinity'),
            'rating': place.get('rating', 0),  # Default rating to 0 if not available
            'open_now': place.get('opening_hours', {}).get('open_now', 'Unknown')
        })

    # Sort stores by rating in descending order and return the top 5
    sorted_stores = sorted(stores, key=lambda x: x['rating'], reverse=True)
    return sorted_stores[:5]
