# Basic imports:
import os
import discord
from discord.ext import commands
import math
import requests
import dotenv
import json
import datetime

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
    async def shorten(self, ctx, url):
        """Shortens a URL. Usage: ?shorten <url>"""
        import gdshortener
        s = gdshortener.ISGDShortener()
        await ctx.send(s.shorten(f'{url}'))


    # Avatar command
    @commands.command()
    async def avatar(self, ctx):
        """Sends you your avatar."""
        avi_url = ctx.author.avatar_url
        aviembed = discord.Embed(title="Avatar of " + ctx.author.name, url=avi_url)
        aviembed.set_image(url=avi_url)
        await ctx.send(embed=aviembed)


    # Calc command
    @commands.command()
    async def calc(self, ctx, n1, op, n2=0):
        """Calculate a mathematical expression. Usage: ?calc <num> <operator> <num>"""
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        if op == "+":
            answer = int(n1) + int(n2)
            equation = f"```{n1}{op}{n2}```"
        elif op == "-":
            answer = int(n1) - int(n2)
            equation = f"```{n1}{op}{n2}```"
        elif op == "*":
            answer = int(n1) * int(n2)
            equation = f"```{n1}{op}{n2}```"
        elif op == "/":
            answer = int(n1) / int(n2)
            equation = f"```{n1}{op}{n2}```"
        elif op == "!" or op == "fac":
            answer = str(math.factorial(int(n1)))
            equation = f'```!{n1}```'
        elif op == "pow":
            answer = math.pow(int(n1), int(n2))
            equation = f"```{n1}" + f"{n2}".translate(SUP) + "```"
        elif op == "sqrt":
            answer = math.sqrt(int(n1))
            equation = f"```√{n1}```"
        else:
            await ctx.send("Invalid operator!")
        calcembed = discord.Embed(title="Calculator", color=0x7ac5c9)
        calcembed.add_field(name="Math equation:", value=equation)
        calcembed.add_field(name="Answer:", value=f"```{answer}```")
        await ctx.send(embed=calcembed)

        # Clear command
    @commands.command()
    async def purge(self, ctx, amount=0):
        """Purge a specified amount of messages. Usage: ?purge <amount>"""
        if amount == 0:
            await ctx.send("Please provide a number.")
        else:
            await ctx.channel.purge(limit=amount + 1)

    # Code command
    @commands.command()
    async def code(self, ctx):
        """Sends bot repo link."""
        await ctx.send("https://github.com/TKLprojects/travbot.py")     

    # Desc command
    @commands.command()
    async def desc(self, ctx, *, cname):
        """Changes voice channel name. Usage: ?desc <name>"""
        channel = ctx.author.voice.channel
        await channel.edit(name=cname)
        await ctx.send(f'Changed channel name to "{cname}"')

    # Weather command
    @commands.command(name="weather")
    async def _weather(self, ctx, city_name):
        """Get weather information about a location. Usage: ?weather <location>"""
        with open("storage/tokens.json") as tokensfile:
            tokenfile = json.load(tokensfile)
            weathertoken = tokenfile['weather']
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = base_url + "key=" + str(weathertoken) + "&q=" + str(city_name)
        try:
            response = requests.get(complete_url)
        except BaseException:
            await ctx.send("no")
        res = response.json()
        # TODO #5 Fix KeyError (can't read token)
        weather = res["current"]
        location = res["location"]
        condition = weather["condition"]

        current_temperature = str(int(weather["temp_c"])) + "°C"
        current_pressure = str(weather["pressure_mb"])[-3:] + "mBar"
        current_humidity = str(weather["humidity"]) + "%"
        image = "https:" + str(condition["icon"])
        weather_timezone = str(location["localtime"])
        weather_location = str(location["name"])
        weather_description = "Description: " + str(condition["text"])
        weather_wind_kph = str(weather["wind_kph"])
        weather_wind_dir = str(weather["wind_dir"])

        weatherembed = discord.Embed(title="Weather for " + weather_location,color=0x7ac5c9)
        weatherembed.set_author(name=f"{self.client.user.name}",icon_url=self.client.user.avatar_url)
        weatherembed.set_footer(text="https://weatherapi.com")
        weatherembed.add_field(name="Temperature:", value=current_temperature)
        weatherembed.add_field(name="Pressure:", value=current_pressure)
        weatherembed.add_field(name="Humidity:", value=current_humidity)
        weatherembed.add_field(name="Wind:",value=weather_wind_kph + " km/h " + weather_wind_dir)
        weatherembed.add_field(name="Time:", value=weather_timezone)
        weatherembed.set_thumbnail(url=image)
        await ctx.send(embed=weatherembed)
    
    @commands.command()
    async def reboot(self, ctx):
        """Reboots the bot, if you run via pm2."""
        await ctx.send("Rebooting...")
        exit()

    # Userinfo command
    @commands.command()
    async def userinfo(self, ctx):
        """Displays info about author."""
        currentDate = datetime.datetime.now()
        avi_url = ctx.author.avatar_url
        infoembed = discord.Embed()
        infoembed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator,icon_url=avi_url)
        infoembed.add_field(name="Status", value=ctx.author.status)
        infoembed.add_field(name="Joined at", value=str(ctx.author.joined_at.day) + "-" + str(ctx.author.joined_at.month) + "-" + str(ctx.author.joined_at.year) + " " + str(ctx.author.joined_at.hour) + ":" + str(ctx.author.joined_at.minute))
        infoembed.add_field(name="Registered at", value=str(ctx.author.created_at.day) + "-" + str(ctx.author.created_at.month) + "-" + str(ctx.author.created_at.year) + " " + str(ctx.author.created_at.hour) + ":" + str(ctx.author.created_at.minute))
        infoembed.add_field(name="Nickname", value=ctx.author.display_name)
        infoembed.set_footer(text=str(currentDate.day) + "-" + str(currentDate.month) + "-" + str(currentDate.year) + " " + str(currentDate.hour) + ":" + str(currentDate.minute) + ":" + str(currentDate.second))
        infoembed.set_thumbnail(url=avi_url)
        await ctx.send(embed=infoembed)
    
    # Serverinfo command
    @commands.command()
    async def serverinfo(self, ctx):
        """Displays info about the current guild."""
        serverembed = discord.Embed(title="Server info")
        serverembed.add_field(name="Server Name",value=ctx.guild.name)
        serverembed.add_field(name="Owner",value=ctx.guild.owner)
        serverembed.add_field(name="Members",value=len(ctx.guild.members))
        serverembed.add_field(name="Channels",value=len(ctx.guild.text_channels + ctx.guild.voice_channels))
        serverembed.add_field(name="Text Channels",value=len(ctx.guild.text_channels))
        serverembed.add_field(name="Voice Channels",value=len(ctx.guild.voice_channels))
        serverembed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=serverembed)

    # Poll command
    # @commands.command()
    # async def poll(self, ctx, question, *options: str):
    #     """Display a poll"""
    #     import time
    #     pollembed = discord.Embed(description=question)
    #     pollembed.set_author(name=f"Poll created by {ctx.message.author}",icon_url=ctx.guild.icon_url)
    #     pollembed.set_footer(text="React to vote.")
    #     reactions = ['✅', '❌']
    #     reactmessage = await ctx.send(embed=pollembed)
    #     for reaction in reactions:
    #         await ctx.message.add_reaction(reaction)

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Utility(client))