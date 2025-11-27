import pandas as pd
import requests
from toolz import isiterable
import time

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
    else:
        return None

    if key is None:
        #Personal API key generated on TomTom website
        key = "SFPtTbSIIRI0fYjw9oMYwxSWUxt0RmXQ"
    elif not isinstance(key, str):
        #Make sure that the given key is a valid value.
        return None

    #Set up variables for API request (base url, ext, etc) so I don't have to type it in each time.
    #Originally just api.tomtom.com, but I think I need to specify exactly what type of search I need
    #to do.
    base_url = "https://api.tomtom.com/search/2/reverseGeocode/"
    ext = "json"

    #Create an empty DF to add the results to
    addresses = pd.DataFrame(columns=['address','status_code'])

    #Send in request
    for i in range(len(lat)):
        #API documentation says position is a comma separated string of latitude and longitude
        #Use fstring to extract each set of coordinates and format into a string
        position = f'{lat[i]},{lng[i]}'
        #Format the payload parameters for the query
        payload = {'position': position, 'ext': ext, 'key': key}
        response = requests.get(base_url, params=payload)

        if response.status_code == 200:
            #Only convert the response to json if it is a successful query
            result = response.json()

            #Format results into a DataFrame and concatenate to the addresses dataframe
            #Access the specific formatted address in the json output. Specifying index 0 of the
            # addresses so that we only access the first query result.
            formatted_result = {'address':result['addresses'][0]['address']['freeformAddress'],
                                'status_code':response.status_code}
            temp_results = pd.DataFrame([formatted_result])
            addresses = pd.concat([addresses,temp_results], axis=0)

        else:
            #Handle unsuccessful queries
            formatted_result = {'address': None, 'status_code': response.status_code}
            temp_results = pd.DataFrame([formatted_result])
            pd.concat([addresses,temp_results], axis=0)

        #Sleep for 0.5 seconds between requests to fix a lagging error tried first with 2 seconds,
        # but that took too long to process, and 0.5 seconds works just fine.
        time.sleep(0.5)

    #Fix indexing because they all become 0 through concatenation.
    addresses.index = range(0,len(addresses))

    return addresses