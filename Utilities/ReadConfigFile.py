from configparser import ConfigParser


def read_config(section, key):
    config = ConfigParser()
    config.read(r'Configurations/config.ini')
    return config.get(section, key)
