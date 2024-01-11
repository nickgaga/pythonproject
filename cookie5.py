from geopy.geocoders import Nominatim

def get_location_info(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
    if location:
        return location.address
    else:
        return "Informazioni sulla posizione non trovate."

def main():
    latitude = 41.4628487
    longitude = 15.5257368

    location_info = get_location_info(latitude, longitude)
    print(f"Coordinate: {latitude}, {longitude}")
    print(f"Posizione: {location_info}")

if __name__ == "__main__":
    main()
