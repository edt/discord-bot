import configparser
import logging
import os

log = logging.getLogger(__file__)


class Settings():

    def __init__(self):

        self.token = None
        self.data_dir = None
        self.load_defaults()

    def load_defaults(self):
        self.token = None
        self.data_dir = None

    def load(self, configfile):

        config = configparser.ConfigParser()

        if not os.path.isfile(configfile):
            return False

        config.read(configfile)

        general = "General"

        gen = config[general]

        self.token = gen.get("token", self.token)
        self.data_dir = gen.get("data_dir", self.data_dir)
        
        return True

def init(configfile):
    
    global config
    config = Settings()
    if not config.load(configfile):
        log.error("Unable to load config")
        return False
    return True