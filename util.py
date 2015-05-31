__author__ = 'james.elkins'

import urllib.request
import json


def validateLocation(location, configManager):
    try:
        location.replace(' ', '_')
        testLocation = jsonObject(location)
        return True
    except:
        return False


def validateAPI(api):
    test_location = jsonObject("San_Francisco_Ca", api)
    try:
        testLocation['current_observation']['weather']
        return True
    except:
        return False

def jsonObject(location, apiKey):

    try:
        request = urllib.request.urlopen('http://api.wunderground.com/api/' + apiKey + '/conditions/q/' + location +'.json')
        jsonString = request.read()
        jsonLocation = json.loads(jsonString.decode())
        return jsonLocation
    except:
        return None