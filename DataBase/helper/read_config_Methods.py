import configparser


# Method to read config file settings
import os.path


def read_config():
    config = configparser.ConfigParser()
    config.read('C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/config.ini')
    return config

