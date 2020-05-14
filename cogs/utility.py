# Basic imports:
import os
import discord
from discord.ext import commands
import math
import requests
import dotenv
from dotenv import load_dotenv
load_dotenv()
weathertoken = os.getenv('WEATHER_TOKEN')

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
        await ctx.send("https://github.com/TKLprojects/travbot.py")     

    # Desc command
    @commands.command()
    async def desc(self, ctx, *, cname):
        channel = ctx.author.voice.channel
        await channel.edit(name=cname)
        await ctx.send(f'Changed channel name to "{cname}"')

    # Weather command
    @commands.command(name="weather")
    async def _weather(self, ctx, city_name):
        # TODO #2 Fix weather command
        """Get weather information about a location. Usage: ?weather <location>"""
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = base_url + "key=" + weathertoken + "&q=" + city_name
        try:
            response = requests.get(complete_url)
        except BaseException:
            await ctx.send("no")
        res = response.json()
        weather = res["current"]
        location = res["location"]
        condition = weather["condition"]

        current_temperature = str(int(weather["temp_c"])) + "°C"
        current_pressure = str(weather["pressure_mb"])[-3:] + "mBar"
        current_humidity = str(weather["humidity"]) + "%"
        image = "https:" + condition["icon"]
        weather_timezone = location["localtime"]
        weather_location = location["name"]
        weather_description = "Description: " + condition["text"]
        weather_wind_kph = str(weather["wind_kph"])
        weather_wind_dir = str(weather["wind_dir"])

        weatherembed = discord.Embed(title="Weather for " + weather_location,color=0x7ac5c9)
        weatherembed.set_author(name=f"{client.user.name}",icon_url=client.user.avatar_url)
        weatherembed.set_footer(text="https://weatherapi.com")
        weatherembed.add_field(name="Temperature:", value=current_temperature)
        weatherembed.add_field(name="Pressure:", value=current_pressure)
        weatherembed.add_field(name="Humidity:", value=current_humidity)
        weatherembed.add_field(name="Wind:",value=weather_wind_kph + " km/h " + weather_wind_dir)
        weatherembed.add_field(name="Time:", value=weather_timezone)
        weatherembed.set_thumbnail(url=image)
        await ctx.send(embed=weatherembed)

# This always needs to be at the end of a cog file:
def setup(client):
    client.add_cog(Utility(client))