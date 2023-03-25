import requests


def getgeoloc():
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCs85_IULmdNSTUj21h_m7FK-15Z1F6V4U'
    r = requests.post(url)
    response = r.json()
    lat = response['location']['lat']
    long = response['location']['lng']
    return lat, long

# getgeoloc()