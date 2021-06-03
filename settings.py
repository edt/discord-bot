import configparser
import logging
import os
import time

log = logging.getLogger(__name__)


class Settings():

    def __init__(self, basedir):

        self.token = None
        self.data_dir = None
        self.cache_dir = None
        self.restart_scheduled = False
        self.reddit_id = None
        self.reddit_secret = None
        self.reddit_agent = None

        self.git_user = None
        self.git_email = None

        self.logfile = None
        self.basedir = basedir
        self.load_defaults()

    def load_defaults(self):
        self.token = None
        self.data_dir = self.basedir + "/data"
        self.cache_dir = self.basedir + "/cache"
        self.restart_scheduled = False
        self.reddit_id = None
        self.reddit_secret = None
        self.reddit_agent = None
        self.git_user = "discord-bot-auto"
        self.git_email = "discord-bot@localhost"

        self.logfile = self.basedir + "/logfile.log"

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

        self.logfile = os.path.expanduser(gen.get("logfile", self.logfile))

        reddit = "reddit"

        red = config[reddit]

        self.reddit_id = red.get("id", self.reddit_id)
        self.reddit_secret = red.get("secret", self.reddit_secret)
        self.reddit_agent = red.get("agent", self.reddit_agent)

        if config.has_section("git"):
            git = config["git"]

            self.git_user = git.get("name", self.git_user)
            self.git_email = git.get("email", self.git_email)

        if config.has_section("Administration"):
            self.admins = config.get('Administration', 'admin').split(',')
        else:
            self.admins = []

        log.info("Admin IDs are: {}".format(self.admins))

        return True


def is_admin(user_id):

    if str(user_id) in config.admins:
        return True
    return False


def init(configfile, basedir):

    global start_time
    start_time = time.time()

    global config
    config = Settings(basedir)
    if not config.load(configfile):
        log.error("Unable to load config")
        return False
    return True
