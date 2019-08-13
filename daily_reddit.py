import discord
from discord.ext import commands

import praw
import secrets

import settings

import inspect


class DailyReddit(commands.Cog):
    """
    Reddit wrapper

    Allows the retrieval of random posts
    Sceduling of daily posts
    """

    def __init__(self, bot):
        self.bot = bot

        self.reddit = praw.Reddit(client_id=settings.config.reddit_id,
                                  client_secret=settings.config.reddit_secret,
                                  user_agent=settings.config.reddit_agent)

        self.generate_functions()

        self.subcommands = ["list", "remove", "add"]

    @commands.group(aliases=['r'])
    async def red(self, ctx, sub):
        """
        DailyReddit main command. Does nothing on its own.
        """
        posts = self.reddit.subreddit(sub).hot(limit=30)
        random_post_number = secrets.randbelow(30)
        for i, post in enumerate(posts):
            if i == random_post_number:
                await ctx.message.channel.send(post.url)
        # ctx.is_
        await ctx.send("bla")

    def __extract(self, subreddit):
        """
        Extract currect top post.
        """
        top_post = self.reddit.subreddit("superbowl").top('day')

        # for post in top_post:
        #     await ctx.send(post.url)

    @red.group()
    async def list(self, ctx):
        """
        List existing reddit posts
        """

        await ctx.send("list")

    @red.group(pass_context=True)
    async def add(self, ctx, time, subreddit):
        """
        Add regular reddit post stuff
        """

        await ctx.send("not implented")

    @red.group(pass_context=True)
    async def remove(self, ctx, entry):
        """
        Remove regular reddit post stuff

        Use the index of the !reddit list command
        """

        await ctx.send("not implemented")

    def generate_cmd(self, cmd, helptext):

        @commands.command(name=cmd)
        async def red_(ctx):
            posts = self.reddit.subreddit(cmd).hot(limit=30)
            random_post_number = secrets.randbelow(30)
            for i, post in enumerate(posts):
                if i == random_post_number:
                    await ctx.message.channel.send(post.url)

        self.red.add_command(red_)

    def generate_functions(self):
        """"""
        cmds = ["superbowl", "foxes", "squirrels"]

        for cmd in cmds:
            self.generate_cmd(cmd, "")

        inspect.getmembers(self.red)


def setup(bot):

    bot.add_cog(DailyReddit(bot))
