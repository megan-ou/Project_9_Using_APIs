import pandas as pd
import requests
from toolz import isiterable

def findAddress(lat, lng, key=None):
    """
    Function that utilizes TomTom's Reverse Geolocating function to find an address based on
    given latitude and longitude coordinates
    Args:
        lat (float): tuple of latitudinal coordinates
        lng (float): tuple of longitudinal coordinates
        key (String): API key to use for the query

    Returns: DataFrame with two columns containing address and status code
    """
    #Error checking
    if isiterable(lat) and isiterable(lng):
        if len(lat) != len(lng):
            return None
        w_lat = lat
        w_lng = lng
    else:
        #If lat and lng have one value, force into a tuple
        w_lat = (lat,)
        w_lng = (lng,)

    if key is None:
        #Personal API key generated on TomTom website
        key = "SFPtTbSIIRI0fYjw9oMYwxSWUxt0RmXQ"
    elif not isinstance(key, str):
        #Make sure that the given key is a valid value.
        return None

    #Set up variables for API request (base url, ext, etc) so I don't have to type it in each time.
    base_url = "https://api.tomtom.com/search/2/reverseGeocode/"
    #Given by the site, I am not too sure what this does
    ext = "json"

    #Send in request
    for i in range(len(w_lat)):
        #API documentation says position is a comma separated string of latitude and longitude
        #Use fstring to extract each set of coordinates and format into a string
        position = f'{w_lat[i]},{w_lng[i]}'
        payload = {'position': position, 'ext': ext, 'key': key}
        response = requests.get(base_url, params=payload)
        print(response.status_code)
        result = response.json()
        print(result)

    #TODO: add in DF, temp return statement
    return None

findAddress(45.575178, -122.726487)