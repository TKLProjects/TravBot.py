# Basic imports:
import discord
from discord.ext import commands
import json
import random
import requests

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
    
    @commands.command()
    async def urban(self, ctx, *, word):
        url = "http://urbanscraper.herokuapp.com/define/"
        completeurl = url + word
        try:
            response = requests.get(completeurl)
        except:
            ctx.send("Couldn't find that word.")

        res = response.json()
        term = res["term"]
        defi = res["definition"]
        example = res["example"]
        word_url = res["url"]
        posttime = res["posted"]
        author = res["author"]
        
        urbanembed = discord.Embed(title=term,url=word_url)
        urbanembed.add_field(name="**Definition:**",value=defi)
        urbanembed.add_field(name="**Example:**",value=example)
        urbanembed.set_footer(text="Author: " + author)
        await ctx.send(embed=urbanembed)



    @commands.command()
    async def emote(self, ctx, emote):
        emoji = discord.Emoji()
        emoteurl = emoji.url
        await ctx.send(emoteurl)

    @commands.command(hidden=True)
    async def tts(self, ctx, *, message):
        await ctx.send(content=message, tts=True)
        

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Fun(client))