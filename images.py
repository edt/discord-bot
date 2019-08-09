import discord
from discord.ext import commands
import random
import os
import logging


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
    async def upload(self, ctx):

        await ctx.send("NO")

    def autogenerate_cmd(self, name, helptext):
        """"""
        @commands.command(name=name,
                          description=helptext)
        async def function(self, ctx):
            cmd_name = "owl"
            folder = "{}/{}/".format(DATA_DIR, cmd_name)
            filename = random.choice(os.listdir(folder))
            log.info(filename)
            await ctx.message.channel.send(file=discord.File(os.path.join(folder, filename)))
            await ctx.send(name)

        function.cog = self
        self.bot.add_command(function)

    def generate_functions(self):
        """ generate bot commands """

        cmds = {"fox": "What does the fox say?",
                "horse": "Meh",
                "wow": "wow",
                "owl": "Fancy owl pics"}

        for cmd, helptext in cmds.items():
            self.autogenerate_cmd(cmd, helptext)


def setup(bot):
    img = Images(bot)
    bot.add_cog(img)
