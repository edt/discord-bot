import discord
from discord.ext import commands


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

            await ctx.send(name)

        function.cog = self
        self.bot.add_command(function)

    def generate_functions(self):
        """ generate bot commands """

        cmds = {"fox": "What does the fox say?",
                "horse": "Meh",
                "wow": "wow"}

        for cmd, helptext in cmds.items():
            self.autogenerate_cmd(cmd, helptext)


def setup(bot):
    img = Images(bot)
    bot.add_cog(img)
