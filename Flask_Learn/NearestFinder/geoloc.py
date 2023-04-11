import requests


def getgeoloc():
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=YOUR_API_KEY'
    r = requests.post(url)
    response = r.json()
    lat = response['location']['lat']
    long = response['location']['lng']
    return lat, long

# getgeoloc()