import math
import pandas as pd
import requests
from toolz import isiterable
import time

def encodeaddress(addr: str) -> str:
    """
    Replaces special characters in address with hexadecimal equivalents
    Args:
        addr (String): string in which characters need replacing

    Returns: reformatted string
    """
    s = str(addr)
    s = s.replace(" ", "%20")
    s = s.replace(",", "%2C")
    s = s.replace("#", "%23")
    return s

def findCoordinates(address, key=None):
    """
    Use TomTom Geocoding API to find coordinates
    Args:
        address: list or pandas.Series
        key (String): TomTom API key to use for the query

    Returns: DataFrame with columns containing lat, lng, address, status code
    """

    #error check parameters
    if isinstance(address, pd.Series):
        addr_list = address.tolist()
    elif isiterable(address) and not isinstance(address, (str, bytes)):
        addr_list = list(address)
    else:
        return None

    #Personal API key generated from TomTom
    #Ensure key is valid
    if key is None:
        key = "Jz895lWf7vUCEUVHSNVRqZw8EIgI9TwG"
    elif not isinstance(key, str):
        return None

    #set base URL
    base_url = "https://api.tomtom.com/search/2/geocode/"
    rows = []

    #send requests one addres at a time
    for addr in addr_list:
        requested_addr = str(addr)

        #replace characters
        encoded_query = encodeaddress(requested_addr)

        #construct full url
        url = f"{base_url}{encoded_query}.json"

        #paramaters
        payload = {
            "key": key,
            "limit": 1
        }

        #default values for unsuccessful query
        lat = math.nan
        lng = math.nan
        out_address = requested_addr
        status = None

        try:
            response = requests.get(url, params=payload)
            status = response.status_code
            time.sleep(.5) #avoid rate limit

            if status == 200:
                result = response.json()
                results = result.get("results", [])

                if results:
                    first_result = results[0]

                    entry_points = first_result.get("entryPoints", [])

                    if entry_points:
                        #find first entry point
                        main_entry = None
                        for ep in entry_points:
                            if ep.get("type") == "main":
                                main_entry = ep
                                break

                        #if no main entry point found, use first
                        if main_entry is None and entry_points:
                            main_entry = entry_points[0]

                        if main_entry:
                            position = main_entry.get("position", {})
                            lat = position.get("lat", math.nan)
                            lng = position.get("lon", math.nan)
                    else:
                        #extract lat and lon from position
                        position = first_result.get("position", {})
                        lat = position.get("lat", math.nan)
                        lng = position.get("lon", math.nan)

                    #extract formatted address
                    address_obj = first_result.get("address", {})
                    out_address = address_obj.get("freeformAddress", requested_addr)

        except requests.exceptions.RequestException:
            #if request fails, keep default values
            pass

        #rows for address
        row = {
            "lat": lat,
            "lng": lng,
            "address": out_address,
            "status_code": status
        }
        rows.append(row)

    #create DataFrame for all rows
    coords = pd.DataFrame(rows)
    coords.index = range(len(coords))

    return coords