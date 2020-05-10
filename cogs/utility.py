# Basic imports:
import discord
from discord.ext import commands

# Cog class:
class Utility(commands.Cog):

#   Forgot what this does, add it:
    def __init__(self, client):
        self.client = client

#   This is an event:
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('This will be printed to the console.')

#   This is a command:
    @commands.command()
    async def ping5(self, ctx):
        await ctx.send("pong nigga")

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Utility(client))