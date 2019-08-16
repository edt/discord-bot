import discord
from discord.ext import commands

import time
import os
import shutil
import subprocess
import settings

import re
import random

import logging

log = logging.getLogger(__name__)


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


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

        def get_size(start_path='.'):
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
        log.info("REBOOT")
        await self.bot.close()

    @commands.command()
    async def shutdown(self, ctx):
        """
        Stop the damn thing
        """
        await ctx.send("My....time....has....come....")
        await self.bot.close()

    @commands.command()
    async def upgrade(self, ctx):
        """
        Upgrade the bot

        This command pull the latest version via git and reboots the bot.
        """

        location = os.path.realpath(__file__)

        with cd(location):

            process_name = subprocess.Popen(["git", "config", "--get", "user.name"], stdout=subprocess.PIPE)
            output = process_name.communicate()
            process_mail = subprocess.Popen(["git", "config", "--get", "user.email"], stdout=subprocess.PIPE)
            output = process_mail.communicate()

            if (process_mail != 0
                    or process_name != 0):
                log.warn("Git user is not defined. Compensating")
                process_name = subprocess.Popen(["git", "config", "user.name", settings.config.git_user],
                                                stdout=subprocess.PIPE)
                process_mail = subprocess.Popen(["git", "config", "user.email", settings.config.git_email],
                                                stdout=subprocess.PIPE)

            process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
            output = process.communicate()

            if process.returncode != 0:
                await ctx.send("```Git failed. Output: {}```".format(output))
            else:
                await ctx.send("```Pulled updates. Rebooting```")
                settings.config.restart_scheduled = True
                await self.bot.close()

    def _roll(self, discord_string):

        regex = r'(\d+)[dDwW](\d+)([+-]\d+)?$'
        dice_string = re.search(regex, discord_string)

        print(dice_string)

        # Proceed if regex matched, send error message otherwise
        if dice_string:
            # initiate random number generator using OS randomizer
            rng = random.SystemRandom()

            # initiate variables and read number of dice and die sides from the first two regex groups
            dice_num = int(dice_string.group(1))
            dice_sides = int(dice_string.group(2))
            dice_mod = 0
            total = 0
            result_list = []

            # if a modifier exists
            if dice_string.group(3):
                dice_mod = int(dice_string.group(3))

            # roll each die individually
            for i in range(0, dice_num):
                roll = rng.randrange(1, dice_sides + 1)
                total += roll
                result_list.append(roll)

            # add modifier and output result
            total += dice_mod

            return True, result_list, dice_mod, total
        else:
            return False, 0, 0, 0

    @commands.command()
    async def roll(self, ctx, *args):
        """
        roll an arbitrary amount of dices.

        Dices may have the format NdX+Y
        N is the number of dices
        X is the type of dice e.g. D20
        Y is an arbitrary modifying int
        """

        for a in args:
            ret, vals, mod, res = self._roll(a)

            if ret:
                await ctx.send("```{a} = {v} + {m} = {r}```".format(a=a, v=vals, m=mod, r=res))
            else:
                await ctx.send("```Could not interpret '{}'```".format(a))


def setup(bot):
    bot.add_cog(General(bot))
