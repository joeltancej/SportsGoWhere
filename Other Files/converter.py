import pyproj

# this code converts x-coordinates and y-coordinates using SVY21 coordinate system to latitude and longtitude

def convertx(x, y):
    xfm = pyproj.Transformer.from_crs('EPSG:3414', 'EPSG:4326')

    a, b = xfm.transform(y, x)
    return a

def converty(x, y):
    xfm = pyproj.Transformer.from_crs('EPSG:3414', 'EPSG:4326')

    a, b = xfm.transform(y, x)
    return b