import geocoder

def getgeoloc():
    g = geocoder.ip('me')
    lat, lng = g.latlng
    return lat, lng