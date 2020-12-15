"""
Personal Discord Bot (Public)
By: monozide

*All functions are used through a discord text channel (works like a terminal)*

This script provides the backend structure for a discord bot.
All communication with the user is done through discord and their
web servers. To host this bot, use heroku or something similar to deploy
or simply host it locally by running this script on your computer.
--------------------------------------------------------------------------------
Features:
    - Game-like elements
        - keeps track of user data and stores it on databases
        - reads, updates, and deletes data in real time
        - perform dynamic actions between multiple users
    - Formatted information responses
        - uses APIs and webscrapers to get data from the web
            - data includes weather, pop culture slang, etc.
        - data is formatted and sent in user-friendly ways
"""
# importing discord bot tools
import discord
from discord.ext import commands

# importing other functionalities
import os
import random
import json
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv

# importing my own scripts
from urban_dictionary_webscraper import urbandict

# initializing environment variables (sensitive information)
# env variables taken from either a .env file or from github/heroku secret keys
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_KEY = os.getenv('WEATHER_KEY')

# initializes the bot and attaches the command prefix specified (accessing a command: prefix + name of command)
client = commands.Bot(command_prefix='.')

# importing bot functionalities from other scripts; discord does this in the form of 'cogs'
# note: I ended up seperating a lot of code from this script and moving it into /cogs for organization
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# displays a message on the shell confirming bot startup


@client.event
async def on_ready():
    print("bot is active")

# removing built-in help command
client.remove_command('help')


# creating error handling for the discord user
@client.event
async def on_command_error(ctx, error):
    """
    Depending on the type of error triggered, alerts the user on
    what they did wrong
    """
    print("Error Ocurred:")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please add specification after your command")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You are not authorized for this command\nPlease register if possible")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command")
    else:
        print(error)
        await ctx.channel.send(f"Congratulations! You triggered an error:\n{error}")


# creating custom help command
@client.command(name='help')
async def help(ctx):
    response = discord.Embed(title='NAZBOT HELP')
    response.add_field(name="/help", value="shows this message", inline=False)
    response.add_field(name="/ping", value="returns the host's delay with server", inline=False)
    response.add_field(name="/8ball + question", value="ask a question and recieve a clasic magic8ball response", inline=False)
    response.add_field(name="/burrito", value="sends a gif of a burrito", inline=False)
    response.add_field(name="/gacha", value="play the NazBot gacha game", inline=False)
    response.add_field(name="/weather + city", value="shows current weather info at a city", inline=False)
    response.add_field(name="/urbandict + search", value="displays the most popular result from urbandictionary.com", inline=False)
    response.set_footer(text='''
    --------------------------------------------------------------------------\n
    if you have ideas/pics to add, just let me know!
    ''')
    await ctx.send(embed=response)


# checks to see if the user that send a message (ctx) is me
def is_it_me(ctx):
    if ctx.author.id == 128236709715378176:
        return True
    if ctx.author.id == 694024881330716722:
        return True
    if ctx.author.id == 184829179110359040:
        return True


# secret command: certain users can clear the specified amount of messages
@client.command()
@commands.check(is_it_me)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


# returns delay between host and discord servers
@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')


# tests sending discord gifs
@client.command(name='burrito')
async def response(ctx):
    await ctx.send("BURRITO IS COOKING...")
    await asyncio.sleep(3)

    await ctx.send(file=discord.File('data/image0.gif'))

# user asks a question; returns a random classic magic8ball answer


@client.command(name="magic8ball")
async def magic8ball(ctx, *, question):

    responses = ['it is certain',
                 'it is decidedly so',
                 'without a doubt',
                 'yes - definitely',
                 'you may rely on it',
                 'as I see it, yes',
                 'most likely',
                 'outlook good',
                 'signs point to yes',
                 'reply hazy, try again',
                 'ask again later',
                 "better not tell you now",
                 'cannot predict now',
                 'concentrate and ask again',
                 "don't count on it",
                 'my reply is no',
                 'my sources say no.',
                 'outlook not so good',
                 'very doubtful']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command(name='weather')
async def weather(ctx, *, city_name):
    """
    Input: ctx (discord message object), city name (string)
    Output: discord embed object containing weather data for the requested city
    """
    my_request = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_KEY}&units=imperial"
    library = requests.get(my_request).json()

    current_temp = library['main']['temp']
    feels_like = library['main']['feels_like']
    daily_min = library['main']['temp_min']
    daily_max = library['main']['temp_max']
    humidity_percentage = library['main']['humidity']
    main_weather = library['weather'][0]['main']
    weather_descript = library['weather'][0]['description']
    city = library['name']
    country = library['sys']['country']
    wind_speed_mph = library['wind']['speed']

    # debug tool: print(f'{city}: {library}')

    time_unix = int(library['dt'])
    sunrise_time = int(library['sys']['sunrise'])
    sunset_time = int(library['sys']['sunset'])

    # determining what weather icon will be used
    if sunrise_time < time_unix < sunset_time:
        embed_color = discord.Color.orange()
        mode = 'day'
    else:
        embed_color = discord.Color.blurple()
        mode = 'night'

    other_weather_bank = ['mist', 'fog']

    with open('data/weather_icons.json', 'r') as file:
        weather_icons = json.load(file)

    if main_weather.lower() in other_weather_bank:
        icon = weather_icons['foggy']
    else:
        icon = weather_icons[mode][main_weather.lower()]

    # determining local time
    time_diff_UTC = int(library['timezone'])
    local_time_unix = time_unix + time_diff_UTC
    local_time_formatted = datetime.utcfromtimestamp(local_time_unix).strftime('%H:%M')

    response = discord.Embed(title=f"**Forecast: {main_weather}**", color=embed_color)
    response.set_author(name=f'Weather Report: {city} at {local_time_formatted}')
    response.add_field(name="Temperature (Fahrenheit): ", value=f"It is currently {current_temp} degrees", inline=False)
    response.add_field(name="__Today's Min__", value=f'{daily_min} degrees')
    response.add_field(name="__Today's Max__", value=f'{daily_max} degrees')
    response.add_field(name="__Feels Like:__", value=f'{feels_like} degrees')
    response.add_field(name="__Humidity__", value=str(humidity_percentage)+"%")
    response.add_field(name="__Wind Speed__", value=f'{wind_speed_mph} mph')
    response.add_field(name="__Description__", value=weather_descript)
    response.set_thumbnail(url=icon)
    response.set_footer(text=f'{city}, {country}\nSource: openweathermap.org')

    await ctx.send(embed=response)


@client.command(name="urbandict")
async def urbandictionary(ctx, *, search_phrase):
    """
    Input: ctx (discord message object), search phrase (string)
    Output: if search phrase is invalid; outputs an error string to the user
            if search phrase is valid; outputs a discord embed object containing formatted
                                       data for the search phrase from urbandictionary.com
    """

    thumbnail = 'https://cdn.discordapp.com/attachments/763613331017039912/784209484758384690/unknown.png'
    library = urbandict(search_phrase)
    if library == -1:
        await ctx.send("Sorry, your search is invalid")

    else:
        response = discord.Embed(title=f'Top Definition: {library["title"].title()}', color=discord.Color.dark_gold())
        response.add_field(name="Definition: ", value=f'{library["definition"]}', inline=False)
        response.add_field(name="Example: ", value=f'*{library["example"]}*', inline=False)
        response.set_footer(
            text=f'By {library["author"]} on {library["date"]}\nUpvotes: {library["likes"]} | Downvotes: {library["dislikes"]}\nSource: urbandictionary.com')
        response.set_thumbnail(url=thumbnail)

        await ctx.send(embed=response)


client.run(TOKEN)
