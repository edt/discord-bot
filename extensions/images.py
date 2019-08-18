import discord
from discord.ext import commands
import random
import os
import logging
import urllib
import requests
import re
# internal modules
import settings
import configparser

log = logging.getLogger("discord-bot")


class Images(commands.Cog):
    """
    Post images from categories
    Register commands for categories dynamically
    """
    def __init__(self, bot):
        self.bot = bot
        self.help_file = os.path.join(settings.config.data_dir, "help_texts.ini")
        self.help_texts = {}
        self.__load_help_texts()
        self.generate_functions()

        self.max_filesize = 8388608  # 8MB in bytes

    def __load_help_texts(self):
        """
        
        """
        if not os.path.isfile(self.help_file):
            log.info("help_texts.ini file does not exist in the data_dir")
            return

        #with open(self.help_file) as f:
        parser = configparser.ConfigParser()

        parser.read(self.help_file)

        t = parser["help_texts"]

        self.help_texts = dict(t)

    def __write_help_texts(self):
        log.info("Writing help texts")
        parser = configparser.ConfigParser()
        parser.add_section("help_texts")

        for key in self.help_texts.keys():
            parser.set("help_texts", key, self.help_texts[key])

        with open(self.help_file, "w") as f:
            parser.write(f)
        log.info("Wrote help texts.")

    @commands.command()
    async def description(self, ctx, name, desc):
        """
        Add a description text to an image category
        """
        exists = False
        # for cmd in self.get_commands():
        #     await ctx.send(cmd.name)
        #     if name == cmd.name:
        #         exists = True
        #         break

        cmd = self.bot.get_command(name)

        if cmd:
            exists = True

        if not exists:
            await ctx.send("Command does not exist! ")
            return
        log.info("Adding help text for command")
        self.help_texts[name] = desc
        log.info("Added. Saving texts.")
        self.__write_help_texts()

        cmd.help = desc
        cmd.brief = desc.partition('\n')[0]
        await ctx.send("```Added description for command {}```".format(name))

    @commands.command()
    async def upload(self, ctx, name, url):
        """
        Upload images to commands

        If a command does not exist, it will be created.
        If a image exists it will not be overwritten.
        Maximum size is discords 8 MB.
        """

        def get_filename_from_cd(cd):
            """
            Get filename from content-disposition
            """
            if not cd:
                return None
            fname = re.findall('filename=(.+)', cd)
            if len(fname) == 0:
                return None
            return fname[0]

        # check the filesize before doing anything
        resGet = requests.get(url, stream=True)

        if int(resGet.headers['Content-length']) > self.max_filesize:

            await ctx.send("The file is too large to be uploaded in the used channel. Please use a different file.")
            await ctx.send("Allowed: {} bytes.This file: {} bytes".format(int(resGet.headers['Content-length']),
                                                                          ctx.guild.filesize_limit))
            return

        if not any(x in resGet.headers['Content-Type'] for x in ["video", "image"]):
            await ctx.send("""```'Content-Type' is neither image not video but '{}' instead.\nUpload aborted.```""".format(resGet.headers['Content-Type']))
            return

        existing_cmds = self.get_existing_subfolders()
        cmd_dir = os.path.join(settings.config.data_dir, name)
        if name not in existing_cmds:
            await ctx.send("Creating command...")

            if not self.create_dir(cmd_dir):
                await ctx.send("Could not create directory. Please contact the bot owner.")
                return
            # add cmd
            self.autogenerate_cmd(name, "")

        # download file
        await ctx.send("Downloading file to server...")
        r = requests.get(url)

        filename = get_filename_from_cd(r.headers.get('content-disposition'))
        if not filename:
            if url.find('/'):
                filename = url.rsplit('/', 1)[1]

        # TODO: filename checking/ uniqueness ensurance

        with open(os.path.join(cmd_dir, filename), 'wb') as f:
            f.write(r.content)

        await ctx.send("Done.")

    def create_dir(self, path):
        """"""
        try:
            os.mkdir(path)
        except OSError:
            log.error("Creation of the directory %s failed" % path)
            return False
        else:
            log.info("Successfully created the directory %s " % path)
            return True

    def autogenerate_cmd(self, name, helptext):
        """
        Adds a single command to the Image category
        """
        log.info("Adding dynamic command {} - {}".format(name, helptext))
        # Add function under the command name -> name
        # else the name 'function' will be used for all
        # and the application will crash
        @commands.command(name=name,
                          description=helptext,
                          brief=helptext.partition('\n')[0])
        async def function(self, ctx):
            folder = os.path.join(settings.config.data_dir, name)
            filename = random.choice(os.listdir(folder))
            log.info(filename)
            await ctx.message.channel.send(file=discord.File(os.path.join(folder, filename)))
            # await ctx.send(name)
        # Add new callback to Image category
        function.cog = self
        # Add function as a callback
        self.bot.add_command(function)

    def get_existing_subfolders(self):
        """
        Returns the names of all subdirectories of the data dir
        """

        return [f.name for f in os.scandir(settings.config.data_dir) if f.is_dir()]

    def generate_functions(self):
        """ generate bot commands for existing image directories"""

        if not os.path.exists(settings.config.data_dir):
            log.error("data_dir does not exist.")
            return
            # os.makedirs(directory)


        for subdir in self.get_existing_subfolders():

            helptext = ""

            if subdir in self.help_texts:
                helptext = self.help_texts[subdir]

            self.autogenerate_cmd(subdir, helptext)


def setup(bot):
    img = Images(bot)
    bot.add_cog(img)
