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

    @commands.command()
    async def react(self, ctx, emote):
        if isinstance(emote, int):
            emotename = client.get_emoji(emote)
        if isinstance(emote, str):
            emotename = discord.utils.get(self.client.emojis, name=emote)
        await ctx.message.add_reaction(emotename)

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
    async def emote(self, ctx, search_term):
        if isinstance(search_term, int):
            emotename = client.get_emoji(search_term)
        if isinstance(search_term, str):
            emotename = discord.utils.get(self.client.emojis, name=search_term)
        await ctx.send(emotename)

    @commands.command(hidden=True)
    async def tts(self, ctx, *, message):
        await ctx.send(content=message, tts=True)
        

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Fun(client))