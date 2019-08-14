import discord
from discord.ext import commands

import os
import praw
import secrets
import sched
import asyncio
import time
from datetime import datetime, timedelta
import settings

from tabulate import tabulate
import json
import sys

import logging

log = logging.getLogger(__file__)

class RedditNewsletter():
    """"""

    def __init__(self, sub, chnl, time):

        self.subreddit = sub
        self.channel_id = chnl
        self.post_time = time

    def to_dict(self):

        return {"subreddit": self.subreddit,
                "channel_id": self.channel_id,
                "post_time": self.post_time}

    def __repr__(self):
        return str(self.to_dict())

    def __str__(self):
        return str(self.__dict__)

    @staticmethod
    def load(json_dump):
        return RedditNewsletter(json_dump["subreddit"],
                                json_dump["channel_id"],
                                json_dump["post_time"])


class DailyReddit(commands.Cog):
    """
    Reddit wrapper

    Allows the retrieval of random posts
    Sceduling of daily posts
    """

    def __init__(self, bot):
        self.bot = bot

        self.praw = praw.Reddit(client_id=settings.config.reddit_id,
                                client_secret=settings.config.reddit_secret,
                                user_agent=settings.config.reddit_agent)

        self.newscycle = []
        self.cache_file = "dailyreddit.json"
        self.__load_newscycle()

        for news in self.newscycle:
            self.__start_newscycle(news)

    @commands.group()
    async def reddit(self, ctx):
        """
        DailyReddit main command. Does nothing on its own.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(ctx.invoked_subcommand)

    @commands.command()
    async def r(self, ctx, sub):
        """
        Post random post of the current top 30 of the named subreddit
        """

        posts = self.praw.subreddit(sub).hot(limit=30)
        random_post_number = secrets.randbelow(30)
        for i, post in enumerate(posts):
            if i == random_post_number:
                await ctx.message.channel.send(post.url)

    def __start_newscycle(self, feed):
        """"""
        print("start_newscycle {}".format(feed.subreddit))

        async def background_task():
            await self.bot.wait_until_ready()
            channel = self.bot.get_channel(int(feed.channel_id))
            print("Checking if closed")
            while not self.bot.is_closed():
                fmt = "%H:%M"
                now = datetime.strftime(datetime.now(), fmt)
                
                # calculate time in seconds
                # if remaining time is negative
                # we calculate it for the next day
                remaining_time = (datetime.strptime(feed.post_time, fmt) 
                                    - datetime.strptime(now, fmt)).total_seconds() 

                if (remaining_time <= 0):
                    remaining_time = (timedelta(hours=24) - (datetime.strptime(now, fmt) - datetime.strptime(post_time, fmt))).total_seconds() 
                
                print("going sleeping {} {}".format(feed.subreddit, remaining_time))
                              
                await asyncio.sleep(remaining_time)
                
                # security check
                # we do not need to post when 
                # task is interupted
                if (self.bot.is_closed()
                        or feed not in self.newscycle):
                    return

                print("sending")
               
                top_post = self.praw.subreddit(feed.subreddit).top('day')
                for p in top_post:
                   await channel.send("Daily {}: {}".format(feed.subreddit, p.url))
                   break
                # wait to ensure we only trigger once per task
                await asyncio.sleep(60)
                
            print("end backgroundtask {}".format(feed.subreddit))

        self.bot.loop.create_task(background_task())

    def __load_newscycle(self):
        """
        Loads cache file
        """
        filename = os.path.join(settings.config.cache_dir, self.cache_file)

        with open(filename) as f:

            data = json.load(f)

        self.newscycle = [RedditNewsletter.load(dump)
                          for dump in data]

    def __save_newscycle(self):
        """
        Saves cache file
        """
        filename = os.path.join(settings.config.cache_dir, self.cache_file)

        with open(filename, 'w+') as f:

            json.dump([o.__dict__ for o in self.newscycle], f, indent=4, sort_keys=True)

    @reddit.command()
    async def list(self, ctx):
        """
        List existing reddit posts
        """
        table = []
        table.append(["Index", "Subreddit", "Post Time"])
        for news in self.newscycle:

            table.append([self.newscycle.index(news),
                          news.subreddit,
                          news.post_time])

        await ctx.send("```{}```".format(tabulate(table, headers="firstrow")))

    @reddit.command()
    async def add(self, ctx, post_time, subreddit):
        """
        Add regular reddit post stuff

        Time format: HH:MM
        Subreddit is reddit.com/r/<string you need>

        !reddit add 08:12 superbowl

        The content will be posted in the channel the request was received.
        """
        fmt = "%H:%M"
        try:
            datetime.strptime(post_time, fmt)
        except ValueError as e:
            await ctx.send("Could not parse time. {}".format(e))
            return
        
        new_feed = RedditNewsletter(subreddit, ctx.channel.id, post_time)
        self.newscycle.append(new_feed)
        self.__save_newscycle()
        self.__start_newscycle(new_feed)
        await ctx.send("Added daily reddit post for {}".format(subreddit))

    @reddit.command()
    async def remove(self, ctx, entry):
        """
        Remove regular reddit post stuff

        Use the index of the !reddit list command
        """
        try:
            index = int(entry)
        except: 
            await ctx.send("Given index is not a number!")
            return

        name = self.newscycle[index].subreddit
        del self.newscycle[index]
        await ctx.send("Removed entry for {}".format(name))

    def generate_cmd(self, cmd, helptext):

        @commands.command(name=cmd)
        async def red_(ctx):
            posts = self.praw.subreddit(cmd).hot(limit=30)
            random_post_number = secrets.randbelow(30)
            for i, post in enumerate(posts):
                if i == random_post_number:
                    await ctx.message.channel.send(post.url)

        self.reddit.add_command(red_)

    def generate_functions(self):
        """"""
        cmds = ["superbowl", "foxes", "squirrels"]

        for cmd in cmds:
            self.generate_cmd(cmd, "")

        inspect.getmembers(self.reddit)


def setup(bot):

    bot.add_cog(DailyReddit(bot))
