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

log = logging.getLogger(__file__)


class Images(commands.Cog):
    """
    Post images from categories
    Register commands for categories dynamically
    """
    def __init__(self, bot):
        self.bot = bot
        self.generate_functions()

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

        if int(resGet.headers['Content-length']) > ctx.guild.filesize_limit:
            await ctx.send("The file  is too large to be uploaded in the used channel. Please use a different file.")
            await ctx.send("Allowed: {} bytes.This file: {} bytes".format(int(resGet.headers['Content-length']),
             ctx.guild.filesize_limit))
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
                filename =  url.rsplit('/', 1)[1]

        print(filename)

        # TODO: filename checking/ uniqueness ensurance

        with open(os.path.join(cmd_dir, filename), 'wb') as f:
            f.write(r.content)

        await ctx.send("Done.")

    def create_dir(self, path):
        """"""
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
            return False
        else:
            print ("Successfully created the directory %s " % path)
            return True


    def autogenerate_cmd(self, name, helptext):
        """
        Adds a single command to the Image category
        """

        # Add function under the command name -> name
        # else the name 'function' will be used for all 
        # and the application will crash
        @commands.command(name=name,
                          description=helptext)
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
        return [f.name for f in os.scandir(settings.config.data_dir) if f.is_dir() ]

    def generate_functions(self):
        """ generate bot commands for existing image directories"""

        for subdir in self.get_existing_subfolders():
            self.autogenerate_cmd(subdir, "")


def setup(bot):
    img = Images(bot)
    bot.add_cog(img)
