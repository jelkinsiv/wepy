__author__ = 'james.elkins'

import configparser
import os.path

configFilePath = os.path.dirname(os.path.realpath(__file__)) + '/config.cfg'


def check_config():

    # check if file exists
    if not os.path.isfile(configFilePath):
        create_config()
        return False
    else:
        return True


def create_config():

    # create and setup the config file
    config_file = open(configFilePath, 'a')
    config_file.write('[key]\n')
    config_file.write('wukey:\n')
    config_file.write('[locations]\n')
    config_file.write('home:\n')
    config_file.write('beach:\n')
    config_file.write('parents:\n')


def get_config(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.cfg')
        return config.get(section, key)
    except Exception as ex:
        print(ex)
        return None


def get_location(location_key):
    return get_config('locations', location_key)


def get_api_key():
    return get_config('key', 'wukey')