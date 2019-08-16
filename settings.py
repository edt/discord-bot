import configparser
import logging
import os
import time

log = logging.getLogger(__name__)


class Settings():

    def __init__(self):

        self.token = None
        self.data_dir = None
        self.cache_dir = None
        self.restart_scheduled = False
        self.reddit_id = None
        self.reddit_secret = None
        self.reddit_agent = None

        self.git_user = None
        self.git_email = None

        self.load_defaults()

    def load_defaults(self):
        self.token = None
        self.data_dir = None
        self.cache_dir = None
        self.restart_scheduled = False
        self.reddit_id = None
        self.reddit_secret = None
        self.reddit_agent = None
        self.git_user = None
        self.git_email = None

    def load(self, configfile):

        config = configparser.ConfigParser()

        if not os.path.isfile(configfile):
            return False

        config.read(configfile)

        general = "General"

        gen = config[general]

        self.token = gen.get("token", self.token)
        self.data_dir = os.path.expanduser(gen.get("data_dir", self.data_dir))
        self.cache_dir = os.path.expanduser(gen.get("cache_dir", self.cache_dir))

        reddit = "reddit"

        red = config[reddit]

        self.reddit_id = red.get("id", self.reddit_id)
        self.reddit_secret = red.get("secret", self.reddit_secret)
        self.reddit_agent = red.get("agent", self.reddit_agent)

        git = config["git"]

        self.git_user = git.get("name", self.git_user)
        self.git_email = git.get("email", self.git_email)

        return True


def init(configfile):

    global start_time
    start_time = time.time()

    global config
    config = Settings()
    if not config.load(configfile):
        log.error("Unable to load config")
        return False
    return True
