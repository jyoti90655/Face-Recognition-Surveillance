import geocoder

def get_current_location():
    location = geocoder.ip('me')
    if location.ok:
        if location.latlng:
            return f"Latitude: {location.latlng[0]}, Longitude: {location.latlng[1]}"
        elif location.address:
            return f"Location: {location.address}"
    return "Location not available"
