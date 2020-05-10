# Basic imports:
import discord
from discord.ext import commands
import json
import random

# Cog class:
class Fun(commands.Cog):

#   Forgot what this does, add it:
    def __init__(self, client):
        self.client = client

#   This is an event:
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('This will be printed to the console.')

#   This is a command:
    @commands.command(name="8ball")
    async def _8ball(self, ctx):
        import random
        linenum = random.randint(1, 20)
        user = "<@" + str(ctx.author.id) + ">"
        with open('./storage/8ball.json') as responses:
            response = json.load(responses)
        await ctx.send(random.choice(response) + user)

    # Figlet command
    @commands.command()
    async def figlet(self, ctx, *, figtext):
        from pyfiglet import Figlet
        fig = Figlet()
        figsend = fig.renderText(figtext)
        await ctx.send(f"```{figsend}```")

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Fun(client))