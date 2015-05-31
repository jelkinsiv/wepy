__author__ = "James Elkins"
__copyright__ = "Copyright 2015"
__credits__ = ["James Elkins"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "James Elkins"
__email__ = "jelkinsiv@gmail.com"
__date__ ="2015/05/24/30"

import urllib.request
import json
import click
import configManager

@click.command()
@click.option('-b', '--beach', is_flag=True, help='View the weather at the beach')
@click.option('-w', '--weekend', is_flag=True, help='View the weather of the next weekend')
@click.option('-p', '--parents', is_flag=True, help='View the weather at parents house')
@click.option('--location', help='View weather at provided location. Use zip or sting with underscores  '
                                 '(ex. San_Francisco)')
def print_weather(beach, weekend, location, parents):

    weatherlocation = configManager.get_location('home')
    if beach:
        weatherlocation = configManager.get_location('beach')
    if parents:
        weatherlocation = configManager.get_location('parents')
    if location:
        weatherlocation = location

    #current conditions
    weather_request = urllib.request.urlopen('http://api.wunderground.com/api/' +
                                             configManager.get_api_key() +
                                             '/geolookup/forecast/forecast10day/conditions/q/' +
                                             weatherlocation + '.json')
    weather_json_string = weather_request.read()
    weather_json = json.loads(weather_json_string.decode())

    locationString = weather_json['current_observation']['display_location']['full']
    currentTemperature = weather_json['current_observation']['temp_f']
    weather = weather_json['current_observation']['weather']
    humidity = weather_json['current_observation']['relative_humidity']

    highTemperature = weather_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
    lowTemperature = weather_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
    rainChance = weather_json['forecast']['simpleforecast']['forecastday'][0]['pop']

    if weekend:

        for day in range(0, len(weather_json['forecast']['simpleforecast']['forecastday'])):
            dayWeather = weather_json['forecast']['simpleforecast']['forecastday'][day]
            dayInfo = weather_json['forecast']['txt_forecast']['forecastday'][day]
            if (dayInfo["title"].split()[0] == "Saturday") or (dayInfo["title"].split()[0] == "Sunday"):
                print('-------------------------------------------')
                print(locationString + ' - ' + dayInfo['title'])
                print(dayInfo['fcttext'])
                print("Chance of Rain: " + dayInfo['pop'] + "%")
    else:
        print(locationString + " - " + weather)
        print(str(currentTemperature) + " F (" + str(highTemperature) + "F / " + str(lowTemperature) + "F)")
        print("Rain: " + str(rainChance) + "%     Humidity: " + humidity)

    weather_request.close()

if __name__ == '__main__':
    if configManager.check_config():
        print_weather()
    else:
        print('Config was created please put API key and location in it. File created at {}'.format(
              configManager.configFilePath))