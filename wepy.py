__author__ = "James Elkins"
__copyright__ = "Copyright 2015"
__credits__ = ["James Elkins"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "James Elkins"
__email__ = "jelkinsiv@gmail.com"
__date__="2015/05/24/30"

import urllib.request
import json
import click
import configparser

#git the config file
config = configparser.ConfigParser()
config.read('config.cfg')

key = config.get('key', 'wuKey')
weatherSymbols = {"sunny": "☀", "cloudy": "☁"}

@click.command()
@click.option('-b', '--beach', is_flag=True, help='View the weather at the beach')
@click.option('-w', '--weekend', is_flag=True, help='View the weather of the next weekend')
@click.option('-p', '--parents', is_flag=True, help='View the weather at parents house')
@click.option('--location', help='View weather at provided location. Use zip or sting with underscores  '
                                 '(ex. San_Francisco)')
def weatherString(beach, weekend, location, parents):

    weatherlocation = '27526'
    if beach:
        weatherlocation = 'Topsail_Beach_NC'
    if parents:
        weatherlocation = '27817'
    if location:
        weatherlocation = location

    #current conditions
    conditionsRequest = urllib.request.urlopen('http://api.wunderground.com/api/'+key+'/conditions/q/'+weatherlocation+'.json')
    conditionsJsonString = conditionsRequest.read()
    conditions = json.loads(conditionsJsonString.decode())

    #current forecast
    forecastRequest = urllib.request.urlopen('http://api.wunderground.com/api/'+key+'/forecast/q/'+weatherlocation+'.json')
    forecastJsonString = forecastRequest.read()
    forecast = json.loads(forecastJsonString.decode())

    if weekend:
        #10dayforcast
        tenDayForecastRequest = urllib.request.urlopen('http://api.wunderground.com/api/'+key+'/forecast10day/q/nc/'+weatherlocation+'.json')
        tenDayForecastJsonString = tenDayForecastRequest.read()
        tenDayForecast = json.loads(tenDayForecastJsonString.decode())

    locationString = conditions['current_observation']['display_location']['full']
    currentTemperature = conditions['current_observation']['temp_f']
    weather = conditions['current_observation']['weather']
    humidity = conditions['current_observation']['relative_humidity']

    highTemperature = forecast['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
    lowTemperature = forecast['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
    rainChance = forecast['forecast']['simpleforecast']['forecastday'][0]['pop']

    if weekend:

        for day in range(0, len(tenDayForecast['forecast']['simpleforecast']['forecastday'])):
            dayWeather = tenDayForecast['forecast']['simpleforecast']['forecastday'][day]
            dayInfo = tenDayForecast['forecast']['txt_forecast']['forecastday'][day]
            if (dayInfo["title"].split()[0] == "Saturday") or (dayInfo["title"].split()[0] == "Sunday"):
                print('-------------------------------------------')
                print(locationString + ' - ' + dayInfo['title'])
                print(dayInfo['fcttext'])
                print("Chance of Rain: " + dayInfo['pop'] + "%")
    else:
        print(locationString + " - " + weather)
        print(str(currentTemperature) + " F (" + str(highTemperature) + "F / " + str(lowTemperature) + "F)")
        print("Rain: " + str(rainChance) + "%     Humidity: " + humidity)

    conditionsRequest.close()
    forecastRequest.close()

if __name__ == '__main__':
    weatherString()