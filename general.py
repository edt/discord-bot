import discord
from discord.ext import commands

import time
import os
import shutil

import settings

class General(commands.Cog):
    """
    General purpose commands
    
    Commands concerning the bot state, administration, etc.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx):

        await ctx.send("reminder")

    @commands.command()
    async def status(self, ctx):
        """
        Give server/bot state.
        
        Given information include:
        Uptime
        Available disk space
        Available images
        """
        
        def get_uptime():
            """
            Returns the number of seconds since the program started.
            """
            # do return startTime if you just want the process start time
            return time.time() - settings.start_time
    
        def uptime_to_str(secs):
            mins, secs = divmod(secs, 60)
            hours, mins = divmod(mins, 60)
            days, hours = divmod(hours, 24)
            return 'D:%d H:%02d M:%02d S:%02d' % (days, hours, mins, secs)
    
        def get_size(start_path = '.'):
            total_size = 0
            for dirpath, _, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            return total_size
    
        folder_size = get_size(settings.config.data_dir)
        disk_free = shutil.disk_usage(settings.config.data_dir)[2]
    
        status_msg = """
        I am alive! But you already knew that....
    
        Uptime: {time}
    
        Static data: {data:6.4f} GB
        Free disk space: {disk:6.4f} GB
        """.format(data=folder_size / (1024.0**3),
                    disk=(disk_free / (1024.0**3)),
                    time=uptime_to_str(get_uptime()))
    
        await ctx.send(status_msg)

    @commands.command()
    async def reboot(self, ctx):
        """
        Reboot the bot.

        Have you tried turning it off and on again?
        """
        await ctx.send("Reboot scheduled.")
        settings.config.restart_scheduled = True
        # closes main loop. actual reboot has to be done there
        await self.bot.close()


def setup(bot):
    bot.add_cog(General(bot))
