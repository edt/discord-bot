import discord
from discord.ext import commands


class General(commands.Cog):
    """glagl"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx):

        await ctx.send("reminder")


def setup(bot):
    bot.add_cog(General(bot))
