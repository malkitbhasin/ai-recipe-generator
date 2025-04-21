from find_grocery_stores import get_nearby_stores


def test_get_nearby_stores():
    # Sample latitude and longitude (e.g., New York City)

    #lat = 40.7128
    #lng = -74.0060

    radius_miles = 5  # Search within 5 miles

    try:
        # Call the function
        stores = get_nearby_stores(radius_miles)

        # Print the results
        if stores:
            print(f"Found {len(stores)} grocery stores:")
            for store in stores:
                print(f"Name: {store['name']}")
                print(f"Address: {store['address']}")
                print(f"Rating: {store['rating']}")
                print(f"Open Now: {store['open_now']}")
                print("-" * 40)
        else:
            print("No grocery stores found.")
    except Exception as e:
        print(f"Error: {e}")

# Run the test
if __name__ == "__main__":
    test_get_nearby_stores()