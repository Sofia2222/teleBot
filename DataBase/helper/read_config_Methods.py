import configparser


# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read('C:/Users/Владелец/PycharmProjects/pythonProject1/config.ini')
    return config
